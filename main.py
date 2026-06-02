import logging
import os
from logging.handlers import RotatingFileHandler
import json
import cohere
from openai import OpenAI
import re
from typing import List, Dict, Any
import base64
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, as_completed, wait
from dotenv import load_dotenv
import requests
import time
import threading
import subprocess
import hashlib
import networkx as nx



load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SRC_PATH=os.getenv("SRC_PATH")
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "doxygen_ai_crew.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Colori ANSI per console
COLORS = {
    "DEBUG": "\033[94m",    # blu chiaro
    "INFO": "\033[92m",     # verde
    "WARNING": "\033[93m",  # giallo
    "ERROR": "\033[91m",    # rosso
    "CRITICAL": "\033[41m", # sfondo rosso
    "RESET": "\033[0m"      # reset
}

# Formatter base (file)
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Formatter colorato per console
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, COLORS["RESET"])
        # Coloriamo solo levelname
        record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"
        return super().format(record)

console_formatter = ColoredFormatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Logger principale
logger = logging.getLogger("DoxygenAICrew")
logger.setLevel(logging.DEBUG)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # INFO+ sulla console
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File Handler
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)



def take_first_lines(files_dict, max_lines=50):
    sampled = {}

    for path, content in files_dict.items():
        try:
            # sicurezza: evita roba non stringa
            if not isinstance(content, str):
                continue

            lines = content.splitlines()

            # prendi solo le prime N righe
            first_lines = "\n".join(lines[:max_lines])

            sampled[path] = first_lines

        except Exception:
            continue

    return sampled


def extract_build_files(files_dict):
    BUILD_KEYWORDS = [
        "makefile",
        "cmakelists.txt",
        "meson.build",
        "build.gradle",
        "pom.xml",
        "package.json",
        "yarn.lock",
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "dockerfile",
        "docker-compose",
        ".github/workflows",
        ".gitlab-ci",
        "jenkinsfile",
        "helm",
        "k8s",
        "chart.yaml"
    ]

    filtered = {}

    for path, content in files_dict.items():
        lower_path = path.lower()

        if any(k in lower_path for k in BUILD_KEYWORDS):
            filtered[path] = content

    return filtered


def to_b64(data: dict) -> str:
    raw = json.dumps(data)
    return base64.b64encode(raw.encode()).decode()





class LLMProvider:
    def __init__(self, name):
        self.name = name

    def chat(self, prompt, max_tokens, temperature):
        raise NotImplementedError

class CohereProvider(LLMProvider):
    def __init__(self, client):
        super().__init__("cohere")
        self.client = client

    def chat(self, prompt, max_tokens, temperature):
        return self.client.chat(
            model="command-xlarge-nightly",
            message=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        ).text

# ----------------------------
# Inizializza LLM cloud (Cohere Chat API)
# ----------------------------
co = cohere.Client(COHERE_API_KEY)



class OpenAIProvider(LLMProvider):
    def __init__(self, client):
        super().__init__("openai")
        self.client = client

    def chat(self, prompt, max_tokens, temperature):
        res = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return res.choices[0].message.content

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

class DeepSeekProvider(LLMProvider):
    def __init__(self, client):
        super().__init__("deepseek")
        self.client = client

    def chat(self, prompt, max_tokens, temperature):
        res = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return res.choices[0].message.content

deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

class FallbackProvider(LLMProvider):
    def __init__(self):
        super().__init__("fallback")

    def chat(self, prompt, max_tokens, temperature):
        return "FALLBACK RESPONSE (no provider available)"

providers = [
    CohereProvider(co),
    OpenAIProvider(openai_client),
    DeepSeekProvider(deepseek_client),
    FallbackProvider()
]


# ----------------------------
# RATE LIMITING GLOBALE
# ----------------------------
class GlobalRateLimiter:
    def __init__(self, base_delay=3.0): # Iniziamo cauti (3s tra chiamate)
        self.min_delay = base_delay
        self.max_delay = 120.0  # Non aspettare mai più di 1 minuto
        self.lock = threading.Lock()
        self.last_call = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            
            if elapsed < self.min_delay:
                sleep_time = self.min_delay - elapsed
                logger.info(f"[RateLimiter] wait {sleep_time:.2f}s")
                time.sleep(sleep_time)
            
            self.last_call = time.time()

    def report_error_429(self):
        """Chiamato quando riceviamo un errore 429"""
        with self.lock:
            # Aumentiamo drasticamente il delay in caso di blocco
            self.min_delay = min(self.min_delay * 1.5, self.max_delay)
            logger.warning(f"[RateLimiter] 429 received. delay increased to {self.min_delay:.2f}s")

    def report_success(self):
        """Chiamato quando la chiamata ha successo"""
        with self.lock:
            # Recupero lento: se tutto va bene, torniamo verso il basso
            if self.min_delay > 3.0:
                self.min_delay = max(self.min_delay * 0.9, 3.0)


rate_limiter = GlobalRateLimiter(base_delay=1.2)



class TokenBudgetManager:

    def __init__(self, model_limit=288000, output_reserve=4000):
        self.model_limit = model_limit
        self.output_reserve = output_reserve

    def count_tokens(self, text: str) -> int:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))

    def check(self, prompt: str, max_tokens: int) -> bool:
        prompt_tokens = self.count_tokens(prompt)
        return (prompt_tokens + max_tokens) <= (self.model_limit - self.output_reserve)

    def safe_max_tokens(self, prompt: str, max_tokens: int) -> int:
        prompt_tokens = self.count_tokens(prompt)

        available = self.model_limit - self.output_reserve - prompt_tokens

        return max(0, min(max_tokens, available))


token_manager = TokenBudgetManager()

def chunk_prompt(prompt: str, max_tokens: int):
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(prompt)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = enc.decode(tokens[i:i + max_tokens])
        chunks.append(chunk)

    return chunks


# ----------------------------
# RISULTATO STRUTTURATO
# ----------------------------
class LLMResult:
    def __init__(self, ok, data=None, raw=None, error=None, attempts=0):
        self.ok = ok
        self.data = data
        self.raw = raw
        self.error = error
        self.attempts = attempts

    def __repr__(self):
        return f"<LLMResult ok={self.ok} attempts={self.attempts} error={self.error}>"

# ----------------------------
# LLM SAFE RUN
# ----------------------------
def llm_run_safe(
    prompt: str,
    max_tokens: int = 800,
    retries: int = 20,
    backoff_base: float = 3.0,
    temperature: float = 0.3,
    expect_json: bool = True,
):
    """
    Robust LLM runner con retry su chunk, backoff adattivo e token safety.
    """
    last_error = None
    prompt_tokens = token_manager.count_tokens(prompt)
    needs_chunking = not token_manager.check(prompt, max_tokens)

    # =========================================================
    # CHUNKED MODE (MAP-REDUCE)
    # =========================================================
    if needs_chunking:
        logger.warning(f"[LLM] Chunk mode activated | tokens={prompt_tokens}")

        chunks = chunk_prompt(prompt, 12000)
        context_memory = ""
        total_attempts = 0

        for i, chunk in enumerate(chunks):

            chunk_success = False

            partial_prompt = None
            text = None

            for attempt in range(retries):

                for provider in providers:
                    try:
                        rate_limiter.wait()

                        partial_prompt = (
                            f"PREVIOUS: {context_memory}\n"
                            f"NEW CHUNK: {chunk}\n"
                            f"TASK: Compress and integrate."
                        )

                        safe_max = token_manager.safe_max_tokens(partial_prompt, max_tokens)

                        response_text = provider.chat(
                            prompt=partial_prompt,
                            max_tokens=safe_max,
                            temperature=temperature
                        )

                        text = (response_text or "").strip()

                        if not text:
                            raise ValueError("Empty chunk response")

                        rate_limiter.report_success()

                        context_memory += "\n" + text
                        total_attempts += 1

                        chunk_success = True
                        break

                    except Exception as e:

                        total_attempts += 1
                        last_error = str(e)

                        if "429" in str(e):
                            logger.warning(f"[CHUNK] {provider.name} quota → switching provider")
                            rate_limiter.report_error_429()
                            continue

                        logger.warning(f"[CHUNK] {provider.name} error: {e}")
                        continue

                if chunk_success:
                    break

            if not chunk_success:
                return LLMResult(
                    ok=False,
                    error=f"Chunk {i} failed",
                    attempts=total_attempts
                )

        # ============================
        # SINTESI FINALE (MERGE FIXED)
        # ============================

        merge_prompt = f"Merge: {context_memory}"
        safe_max = token_manager.safe_max_tokens(merge_prompt, max_tokens)

        last_error = None

        for attempt in range(1, retries + 1):  # global retry

            rate_limiter.wait()

            for provider in providers:  # failover providers

                try:
                    response_text = provider.chat(
                        prompt=merge_prompt,
                        max_tokens=safe_max,
                        temperature=temperature
                    )

                    text = (response_text or "").strip()

                    if not text:
                        raise ValueError("Empty merge response")

                    rate_limiter.report_success()

                    parsed = extract_json(text) if expect_json else text

                    return LLMResult(
                        ok=True,
                        data=parsed,
                        raw=text,
                        attempts=attempt
                    )

                except Exception as e:
                    last_error = str(e)

                    if "429" in str(e):
                        logger.warning(f"[MERGE] {provider.name} 429 → retry provider")
                        rate_limiter.report_error_429()
                        continue

                    logger.warning(f"[MERGE] {provider.name} error: {e}")
                    continue

            # se tutti i provider falliscono → backoff globale
            sleep_time = backoff_base ** (attempt - 1)
            logger.warning(f"[MERGE] all providers failed → retry in {sleep_time:.2f}s")
            time.sleep(sleep_time)

        return LLMResult(
            ok=False,
            error=last_error,
            attempts=retries
        )
        
    # =========================================================
    # NORMAL MODE (NO CHUNKING)
    # =========================================================
    last_error = None

    for attempt in range(1, retries + 1):
        rate_limiter.wait()

        for provider in providers:
            try:
                safe_max = token_manager.safe_max_tokens(prompt, max_tokens)

                response_text = provider.chat(
                    prompt=prompt,
                    max_tokens=safe_max,
                    temperature=temperature
                )

                text = (response_text or "").strip()

                if not text:
                    raise ValueError(f"{provider.name}: empty response")

                parsed = extract_json(text) if expect_json else text

                if expect_json and parsed is None:
                    raise ValueError(f"{provider.name}: invalid JSON")

                rate_limiter.report_success()

                return LLMResult(
                    ok=True,
                    data=parsed,
                    raw=text,
                    attempts=attempt
                )

            # =====================================================
            # PROVIDER-LEVEL EXCEPTIONS
            # =====================================================
            except Exception as e:
                last_error = e
                msg = str(e).lower()

                if "429" in msg or "quota" in msg or "rate limit" in msg:
                    logger.warning(
                        f"[LLM-NORMAL MODE] {provider.name} quota/rate-limit → switching provider"
                    )
                    rate_limiter.report_error_429()
                    continue

                if "empty response" in msg or "invalid json" in msg:
                    logger.warning(f"[LLM-NORMAL MODE] {provider.name} bad output → switching provider")
                    continue

                logger.warning(f"[LLM-NORMAL MODE] {provider.name} error: {e}")
                continue

        # =========================================================
        # ALL PROVIDERS FAILED IN THIS ATTEMPT → BACKOFF
        # =========================================================
        sleep_time = backoff_base ** (attempt - 1)
        logger.warning(f"[LLM-NORMAL MODE] all providers failed → retrying in {sleep_time:.2f}s")
        time.sleep(sleep_time)

    # =========================================================
    # FINAL FAILURE
    # =========================================================
    logger.error("[LLM] Max retries reached in NORMAL MODE.")
    return LLMResult(
        ok=False,
        error=str(last_error),
        attempts=retries
    )

def extract_json(text: str):
    """
    Robust JSON extractor for LLM responses.
    Supports:
    - markdown fences
    - text before/after JSON
    - arrays or dicts
    - trailing commas
    - malformed wrapping text
    """

    if not text:
        return None

    import json
    import re

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # normalize quotes occasionally broken
    text = text.replace("\u201c", '"').replace("\u201d", '"')

    # ---------------------------------------------------
    # TRY DIRECT FULL JSON
    # ---------------------------------------------------
    try:
        return json.loads(text)
    except:
        pass

    # ---------------------------------------------------
    # FIND FIRST JSON OBJECT / ARRAY
    # ---------------------------------------------------
    candidates = []

    stack = []
    start = None

    for i, ch in enumerate(text):

        if ch in "{[":
            if not stack:
                start = i
            stack.append(ch)

        elif ch in "}]":
            if stack:
                stack.pop()

                if not stack and start is not None:
                    candidates.append(text[start:i+1])
                    start = None

    # ---------------------------------------------------
    # TRY ALL CANDIDATES
    # ---------------------------------------------------
    for c in candidates:

        # remove trailing commas
        cleaned = re.sub(r",(\s*[}\]])", r"\1", c)

        try:
            return json.loads(cleaned)
        except:
            continue

    return None

def llm_run(prompt: str, max_tokens: int = 800) -> str:
    logger.info(f"LLM run (prime 100 char): {prompt[:100]}...")

    res = llm_run_safe(
        prompt=prompt,
        max_tokens=max_tokens,
        expect_json=False
    )

    if not res.ok:
        raise RuntimeError(f"LLM failed after {res.attempts} attempts: {res.error}")

    return res.data

# ----------------------------
# Lettura ricorsiva file
# ----------------------------
def read_project_files(base_path: str, max_chars_per_file: int = 1000) -> dict:
    project_files = {}
    for root, _, files in os.walk(base_path):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_path)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                    project_files[rel_path] = file.read(max_chars_per_file)
            except Exception as e:
                project_files[rel_path] = f"<ERRORE lettura: {e}>"
    return project_files

# ----------------------------
# Lettura examples strutturati
# ----------------------------
def read_examples(base_path: str, max_chars_per_file: int = 1000) -> dict:
    examples = {}

    for project_name in os.listdir(base_path):
        project_dir = os.path.join(base_path, project_name)
        if not os.path.isdir(project_dir):
            continue

        example_src = {}
        example_template = {}

        for root, _, files in os.walk(project_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, project_dir)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read(max_chars_per_file)

                        # Separiamo src e template
                        if rel_path.startswith("src"):
                            example_src[rel_path] = content
                        else:
                            example_template[rel_path] = content

                except Exception as e:
                    example_template[rel_path] = f"<ERRORE: {e}>"

        examples[project_name] = {
            "src": example_src,
            "template": example_template
        }

    return examples

# ----------------------------
# Scrittura template adattato su disco
# ----------------------------
def save_template_to_disk(template_dict: dict, out_dir: str):
    if os.path.exists(out_dir):
        # opzionale: pulizia
        import shutil
        shutil.rmtree(out_dir)

    os.makedirs(out_dir, exist_ok=True)

    for path, content in template_dict.items():
        full_path = os.path.join(out_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            logger.error(f"[ERROR write] {full_path}: {e}")


def generate_doxygen_base(project_root: str, out_dir: str):
    """
    Genera:
    - Doxyfile base
    - header.html
    - footer.html
    - stylesheet.css
    usando Doxygen reale.
    """

    import subprocess
    import os

    os.makedirs(out_dir, exist_ok=True)

    # 1 genera Doxyfile
    subprocess.run(
        ["doxygen", "-g", os.path.join(out_dir, "Doxyfile")],
        check=True
    )

    doxyfile = os.path.join(out_dir, "Doxyfile")

    # 2 abilita header/footer generation
    with open(doxyfile, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "GENERATE_HTML = YES",
        "GENERATE_HTML = YES\nHTML_HEADER = header.html\nHTML_FOOTER = footer.html\nHTML_STYLESHEET = stylesheet.css"
    )

    with open(doxyfile, "w", encoding="utf-8") as f:
        f.write(content)

    # 3 esegue doxygen per generare i template
    subprocess.run(
        ["doxygen", doxyfile],
        cwd=out_dir,
        check=True
    )

    generated = {}

    html_dir = os.path.join(out_dir, "html")

    for name in ["header.html", "footer.html", "stylesheet.css"]:
        path = os.path.join(html_dir, name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                generated[name] = f.read()

    return {
        "doxyfile_path": doxyfile,
        "assets": generated
    }


def prefilter_files(files_dict):
    candidates = {}

    for path, content in files_dict.items():
        lower = path.lower()

        # filtra file troppo grandi
        if len(content) > 200_000:
            continue

        # keyword leggere su path
        if any(k in lower for k in [
            "build", "make", "cmake", "gradle", "pom",
            "package", "docker", "config", "ci", "pipeline"
        ]):
            candidates[path] = content
            continue

        # estensioni tipiche config
        if lower.endswith((".json", ".yml", ".yaml", ".xml", ".toml")):
            candidates[path] = content

    return candidates




def extract_build_candidates(files_dict, classification):
    candidates = {}

    for f in classification.get("files", []):
        if f.get("type") in [
            "build", "dependency", "config", "ci_cd", "container"
        ] and f.get("confidence", 0) > 0.5:

            path = f["path"]

            if path in files_dict:
                candidates[path] = files_dict[path][:3000]  # truncate sicurezza

    return candidates



class FileClassifier:
    """
    Servizio unico per classificare file.
    Ottimizzato con:
    - fast classifier (no LLM)
    - cache
    - batch LLM fallback
    """

    TYPES = [
        "source", "build", "config", "test",
        "markup", "script", "documentation", "other"
    ]

    def __init__(self):
        self.cache = {}

    # ----------------------------
    # FAST CLASSIFIER (NO LLM)
    # ----------------------------
    def fast_classify(self, file_path, file_lines):
        path = file_path.lower()
        name = path.split("/")[-1]

        # EXTENSION BASED
        if path.endswith((".py", ".js", ".ts", ".cpp", ".c", ".java", ".go", ".rs")):
            return self._result(file_path, "source", path.split(".")[-1], 0.95)

        if path.endswith((".md", ".rst", ".txt")):
            return self._result(file_path, "documentation", "text", 0.95)

        if path.endswith((".html", ".xml", ".json", ".yaml", ".yml")):
            return self._result(file_path, "markup", path.split(".")[-1], 0.9)

        if path.endswith((".sh", ".bash")):
            return self._result(file_path, "script", "shell", 0.9)

        # NAME BASED
        if name in ["dockerfile"]:
            return self._result(file_path, "build", "docker", 0.95)

        if name in ["package.json"]:
            return self._result(file_path, "build", "npm", 0.95)

        if name in ["requirements.txt"]:
            return self._result(file_path, "dependency", "pip", 0.95)

        if "test" in path:
            return self._result(file_path, "test", "", 0.8)

        return None  # fallback a LLM

    def _result(self, path, t, subtype, conf):
        return {
            "path": path,
            "type": t,
            "subtype": subtype,
            "confidence": conf
        }

    # ----------------------------
    # LLM BATCH
    # ----------------------------
    def classify_files_with_llm(self, files_dict):
        if not files_dict:
            return {"files": []}

        snippets = take_first_lines(files_dict, 50)
        files_b64 = to_b64(snippets)

        prompt = f"""
        You are an expert file classification engine.

        FILES_B64:
        {files_b64}

        For each file classify:

        - type: build | dependency | config | ci_cd | container | source | documentation | script | test | markup | other
        - subtype
        - confidence

        Return JSON:
        {{
            "files": [
                {{
                    "path": "",
                    "type": "",
                    "subtype": "",
                    "confidence": 0.0
                }}
            ]
        }}
        """

        result = llm_run(prompt, max_tokens=1200)
        parsed = extract_json(result)

        if not parsed:
            return {"files": []}
        

        return parsed

    def classify_files_batch(self, files_dict, max_lines=50):
        first_lines_dict = take_first_lines(files_dict, max_lines)

        results = []
        llm_candidates = {}

        # STEP 1: cache + fast classifier
        for path, lines in first_lines_dict.items():

            # cache
            if path in self.cache:
                results.append(self.cache[path])
                continue

            # fast classifier
            fast = self.fast_classify(path, lines)

            if fast:
                self.cache[path] = fast
                results.append(fast)
            else:
                llm_candidates[path] = lines

        # STEP 2: LLM solo per incerti
        if llm_candidates:
            llm_result = self.classify_files_with_llm(llm_candidates)
            files = llm_result.get("files", [])

            for f in files:
                self.cache[f["path"]] = f
                results.append(f)

        return results

_classifier_lock = threading.Lock()
_classifier_instance = None

def get_file_classifier() -> FileClassifier:
    """
    Restituisce l'istanza singleton di FileClassifier.
    Thread-safe.
    """
    global _classifier_instance
    if _classifier_instance is None:
        with _classifier_lock:
            if _classifier_instance is None:
                _classifier_instance = FileClassifier()
    return _classifier_instance

class GitHubManager:
    def __init__(self, github_token: str, username: str = None):
        self.github_token = github_token
        self.username = username
        self.headers = {"Authorization": f"token {self.github_token}"}

    # ----------------------------
    # Helper: recupera info README + badge CI
    # ----------------------------
    def _get_readme_info(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            return {"readme_length": 0, "ci_badges": []}
        data = r.json()
        content = base64.b64decode(data.get("content", "")).decode(errors="ignore")
        readme_length = len(content)

        # Cerca badge CI (Travis, GitHub Actions, CircleCI, Jenkins)
        ci_badges = re.findall(
            r"!\[.*?\]\(.*?(travis-ci\.org|github\.com/.*/.*/actions|circleci\.com|jenkins\.io).*?\)",
            content,
            re.IGNORECASE
        )
        return {"readme_length": readme_length, "ci_badges": ci_badges}

    # ----------------------------
    # Recupera repo utente con paginazione
    # ----------------------------
    def get_user_repos(self, max_repos=1):
        if not self.username:
            return []

        repos = []
        page = 1
        per_page = min(max_repos, 100)

        while len(repos) < max_repos:
            url = f"https://api.github.com/users/{self.username}/repos"
            params = {"sort": "updated", "per_page": per_page, "page": page}
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                break
            data = r.json()
            if not data:
                break

            for repo in data:
                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue
                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])
                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "watchers": repo["watchers_count"],
                    "language": repo.get("language"),
                    "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "fork": repo["fork"],
                    "archived": repo["archived"],
                    "is_template": repo.get("is_template", False),
                    **readme_info
                })
                if len(repos) >= max_repos:
                    break
            page += 1

        return repos

    # ----------------------------
    # Recupera repo globali popolari con paginazione
    # ----------------------------
    def get_global_repos(self, min_stars=5000, max_repos=1):
        repos = []
        page = 1
        per_page = min(max_repos, 100)

        while len(repos) < max_repos:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"stars:>{min_stars}",
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
                "page": page
            }
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                break
            data = r.json()
            if not data.get("items"):
                break

            for repo in data["items"]:
                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue
                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])
                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "watchers": repo["watchers_count"],
                    "language": repo.get("language"),
                    "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "fork": repo["fork"],
                    "archived": repo["archived"],
                    "is_template": repo.get("is_template", False),
                    **readme_info
                })
                if len(repos) >= max_repos:
                    break
            page += 1

        return repos

    # ----------------------------
    # Merge intelligente delle repo
    # ----------------------------
    @staticmethod
    def merge_repos(*repo_lists, max_total=10):
        seen = set()
        merged = []

        for repo_list in repo_lists:
            for repo in repo_list:
                key = (repo["owner"], repo["repo"])
                if key not in seen:
                    seen.add(key)
                    merged.append(repo)
                if len(merged) >= max_total:
                    return merged
        return merged

    # ----------------------------
    # Scopre repo rilevanti dal contesto
    # ----------------------------
    def discover_repos_from_context(self, crew_context: dict, max_repos=1):
        lang = crew_context.get("LanguageDetector", {}).get("primary_language", "")
        build = crew_context.get("BuildSystemDetector", {}).get("build_systems", [])

        base_queries = []

        # ------------------------
        # QUERY 1: linguaggio + stars
        # ------------------------
        if lang:
            base_queries.append(f"language:{lang}")

        base_queries.append("stars:>1000")

        # ------------------------
        # QUERY 2: API / framework hint
        # ------------------------
        if lang:
            base_queries.append(f"language:{lang} topic:api")
            base_queries.append(f"language:{lang} topic:web")

        # ------------------------
        # QUERY 3: build system SOLO se utile
        # ------------------------
        if build:
            b = build[0].lower()
            if b in ["pip", "poetry", "pipenv", "setuptools"]:
                base_queries.append(f"language:{lang} topic:python")

        # ------------------------
        # QUERY 4: documentation (più soft)
        # ------------------------
        base_queries.append("in:readme documentation")
        base_queries.append("topic:documentation")

        repos = []
        seen = set()

        for query in base_queries:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": max_repos
            }

            r = requests.get(url, headers=self.headers, params=params)

            if r.status_code != 200:
                continue

            items = r.json().get("items", [])

            for repo in items:
                key = (repo["owner"]["login"], repo["name"])

                if key in seen:
                    continue

                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue

                seen.add(key)

                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])

                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "language": repo.get("language"),
                    **readme_info
                })

                if len(repos) >= max_repos:
                    return repos

        return repos

    # ----------------------------
    # Merge intelligente delle repo
    # ----------------------------
    @staticmethod
    def merge_repos(*repo_lists, max_total=6):
        seen = set()
        merged = []

        for repo_list in repo_lists:
            for repo in repo_list:
                key = (repo["owner"], repo["repo"])
                if key not in seen:
                    seen.add(key)
                    merged.append(repo)
                if len(merged) >= max_total:
                    return merged
        return merged


    def fetch_repo_md_files(
        self,
        owner: str,
        repo: str,
        branch: str = None,
        max_files: int = 30,
        max_chars_per_file: int = 12000
    ) -> dict:
        """
        Scarica tutti i file markdown del repository.

        Return:
        {
            "README.md": "...",
            "docs/install.md": "...",
            ...
        }

        Features:
        - prova branch automatico main/master/default_branch
        - recursive tree scan
        - solo file .md/.markdown/.mdx
        - limita numero file
        - limita dimensione contenuto
        """

        logger.info(f"[GitHubManager] Fetch markdown files: {owner}/{repo}")

        md_files = {}

        # -----------------------------------
        # STEP 1 - Recupera metadata repo
        # -----------------------------------
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        r = requests.get(repo_url, headers=self.headers, timeout=20)

        if r.status_code != 200:
            logger.warning(
                f"[GitHubManager] Cannot read repo metadata {owner}/{repo} "
                f"status={r.status_code}"
            )
            return {}

        repo_info = r.json()

        default_branch = repo_info.get("default_branch", "main")

        if not branch:
            branch = default_branch

        # -----------------------------------
        # STEP 2 - Tree ricorsivo
        # -----------------------------------
        tree_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/git/trees/{branch}?recursive=1"
        )

        r = requests.get(tree_url, headers=self.headers, timeout=30)

        if r.status_code != 200:
            logger.warning(
                f"[GitHubManager] Tree fetch failed {owner}/{repo} "
                f"branch={branch} status={r.status_code}"
            )
            return {}

        data = r.json()
        tree = data.get("tree", [])

        logger.info(
            f"[GitHubManager] {owner}/{repo} tree objects: {len(tree)}"
        )

        # -----------------------------------
        # STEP 3 - Filtra markdown files
        # -----------------------------------
        markdown_paths = []

        for item in tree:
            if item.get("type") != "blob":
                continue

            path = item.get("path", "")
            lower = path.lower()

            if lower.endswith((".md", ".markdown", ".mdx")):
                markdown_paths.append(path)

        markdown_paths = markdown_paths[:max_files]

        logger.info(
            f"[GitHubManager] {owner}/{repo} markdown files found: "
            f"{len(markdown_paths)}"
        )

        # -----------------------------------
        # STEP 4 - Scarica contenuti raw
        # -----------------------------------
        for path in markdown_paths:

            raw_url = (
                f"https://raw.githubusercontent.com/"
                f"{owner}/{repo}/{branch}/{path}"
            )

            try:
                rr = requests.get(raw_url, headers=self.headers, timeout=20)

                if rr.status_code == 200:
                    text = rr.text[:max_chars_per_file]
                    md_files[path] = text

                    logger.info(
                        f"[GitHubManager] OK {owner}/{repo}/{path} "
                        f"({len(text)} chars)"
                    )

                else:
                    logger.warning(
                        f"[GitHubManager] RAW fail {path} "
                        f"status={rr.status_code}"
                    )

            except Exception as e:
                logger.warning(
                    f"[GitHubManager] Error downloading {path}: {e}"
                )

        logger.info(
            f"[GitHubManager] Completed {owner}/{repo}: "
            f"{len(md_files)} markdown files"
        )

        return md_files


# ----------------------------
# Base Agent
# ----------------------------
class Agent:
    def __init__(self, name: str, depends_on=None):
        self.name = name
        self.depends_on = depends_on or []
        self.lock = None

    def get_agent_output(self, crew_context: dict, agent_name: str) -> dict:
        # Usiamo il lock per una lettura sicura
        with self.lock:
            results = crew_context.get("results", {})
            return results.get(agent_name, {})

    def save_result(self, crew_context: dict, data: dict):
        # Usiamo il lock per una scrittura sicura
        with self.lock:
            if "results" not in crew_context:
                crew_context["results"] = {}
            crew_context["results"][self.name] = data

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]) -> Any:
        raise NotImplementedError()
    
    def get_task(self, task, key, default=None):
        return task.get(key, default)

    def get_metadata(self, crew_context):
        return crew_context.get("metadata", {})

    def safe_get(self, data, key, default=None):
        if not isinstance(data, dict):
            return default
        return data.get(key, default)


# ----------------------------
# Detector and Analyzer Agent
# ----------------------------
class ProjectTreeAnalyzer(Agent):

    def __init__(self):
        super().__init__("ProjectTreeAnalyzer")

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):

        logger.info(f"[{self.name}] start running")

        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        
        # Estrae l'elenco dei percorsi dei file per creare l'albero
        file_paths = list(files_dict.keys())

        prompt = f"""
            You are a senior software architect.

            Analyze the FILE PATHS of a software project.

            Infer the project structure and directory organization.

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILE_PATHS:
            {json.dumps(file_paths, indent=2)}

            Infer:

            - directory_tree
            - root_modules
            - src_directory_present
            - tests_directory_present
            - docs_directory_present
            - config_directory_present
            - scripts_directory_present
            - packaging_files
            - average_directory_depth
            - project_layout_type
            (monolithic | modular | layered | microservices | library | embedded)

            Return STRICT JSON:

            {{
            "directory_tree": {{}},
            "root_modules": [],
            "src_directory_present": true,
            "tests_directory_present": true,
            "docs_directory_present": true,
            "config_directory_present": true,
            "scripts_directory_present": true,
            "packaging_files": [],
            "average_directory_depth": 0,
            "project_layout_type": "",
            "directory_conventions": []
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            If something cannot be deduced return null.
            """

        result = llm_run(prompt, max_tokens=1200)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class LanguageDetector(Agent):

    def __init__(self):
        super().__init__("LanguageDetector")

    def run(self, task, crew_context):

        logger.info(f"[{self.name}] start running")

        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # ----------------------------
        # 2. Estensioni file (veloce)
        # ----------------------------
        file_extensions = list({
            path.split(".")[-1].lower()
            for path in files_dict.keys()
            if "." in path
        })

        # ----------------------------
        # 3. Sampling contenuto
        # ----------------------------
        sampled_files = take_first_lines(files_dict, 50)
        sampled_b64 = to_b64(sampled_files)

        # ----------------------------
        # PROMPT OTTIMIZZATO
        # ----------------------------
        prompt = f"""
            You are a programming language detection engine.

            You are given:

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILE EXTENSIONS:
            {file_extensions}

            SAMPLE FILE CONTENTS (first lines only, base64):
            {sampled_b64}

            Detect:

            - primary_language
            - secondary_languages
            - scripting_languages
            - configuration_languages
            - markup_languages
            - language_standards (C11, C++17, Python3, etc)
            - multi_language_project
            - interpreted_or_compiled
            - codebase_size_estimate

            Return STRICT JSON:

            {{
            "primary_language": "",
            "secondary_languages": [],
            "scripting_languages": [],
            "configuration_languages": [],
            "markup_languages": [],
            "language_standards": {{}},
            "multi_language_project": true,
            "interpreted_or_compiled": "",
            "codebase_size_estimate": "",
            "confidence": 0.0
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            Return null where unknown.
        """

        result = llm_run(prompt, max_tokens=900)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class BuildSystemDetector(Agent):

    def __init__(self):
        super().__init__("BuildSystemDetector")

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        
        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        if not files_dict:
            result = {"error": "no_files"}
            crew_context[self.name] = result
            return result

        # ----------------------------
        # STEP 1: PREFILTER (cheap)
        # ----------------------------
        filtered_files = prefilter_files(files_dict)

        # fallback sicurezza
        if not filtered_files:
            filtered_files = files_dict


        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(filtered_files, max_lines=50)

        # Step 3: estrarre solo file rilevanti per build/dependency/config
        build_candidates = {
            f["path"]: filtered_files[f["path"]]
            for f in classified_files
            if f["type"] in ["build", "dependency", "config", "ci_cd", "container"] and f.get("confidence", 0) > 0.5
        }

        # fallback se vuoto
        if not build_candidates:
            build_candidates = filtered_files

        snippets = take_first_lines(build_candidates, 100)
        files_b64 = to_b64(snippets)

        # ----------------------------
        # STEP 4: ANALISI BUILD SYSTEM
        # ----------------------------
        prompt = f"""
        You are an expert build systems analyzer.

        PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

        FILES_B64 contains relevant build/configuration files.

        {files_b64}

        Detect:

        - build_systems
        - build_files
        - build_commands
        - test_commands
        - package_managers
        - ci_cd_detected
        - containerization
        - build_complexity
        - cross_platform_support

        Return JSON:

        {{
            "build_systems": [],
            "build_files": [],
            "build_commands": [],
            "test_commands": [],
            "package_managers": [],
            "ci_cd_detected": [],
            "containerization": [],
            "build_complexity": "",
            "cross_platform_support": true
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=900)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        # ----------------------------
        # DEBUG INFO (OPZIONALE)
        # ----------------------------
        parsed["_meta"] = {
            "total_files": len(files_dict),
            "filtered_files": len(filtered_files),
            "build_candidates": len(build_candidates)
        }

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class DependencyDetector(Agent):

    def __init__(self):
        super().__init__("DependencyDetector")

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        
        # 1. Recupera i dati di input dal task
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)

        # filtra solo file utili per analisi dipendenze
        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["build", "config", "source"]
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        prompt = f"""
            You are a software dependency analysis engine.

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILES_B64:
            {files_b64}

            Detect:

            - runtime_dependencies
            - build_dependencies
            - development_dependencies
            - external_services
            - system_dependencies
            - package_managers
            - dependency_versions

            Return JSON:

            {{
            "runtime_dependencies": [],
            "build_dependencies": [],
            "development_dependencies": [],
            "external_services": [],
            "system_dependencies": [],
            "package_managers": [],
            "dependency_versions": {{}},
            "dependency_management_strategy": ""
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.


            """

        result = llm_run(prompt, max_tokens=1600)
        parsed = extract_json(result) or {"error":"invalid_json","raw":result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

    

class CodeArchitectureAnalyzer(Agent):

    def __init__(self):
        super().__init__("CodeArchitectureAnalyzer")

    
    @staticmethod
    def find_relevant_code(section_name, repo_ast, code_graph):

        prompt = f"""
        You are mapping documentation sections to source code.

        SECTION:
        {section_name}

        AVAILABLE CODE GRAPH:
        {json.dumps(code_graph, indent=2)}

        TASK:

        Find ONLY relevant code entities for this documentation section.

        Prefer:
        - semantic similarity
        - exact naming
        - architectural relevance
        - usage importance

        Return STRICT JSON:

        {{
            "functions": [],
            "classes": [],
            "files": [],
            "confidence": 0.0,
            "coverage": "none|partial|good|full",
            "ranking": [],
            "reasoning": ""
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=1200)

        parsed = extract_json(result)

        if not parsed:
            return {
                "functions": [],
                "classes": [],
                "files": [],
                "confidence": 0.0,
                "coverage": "none",
                "ranking": [],
                "reasoning": "No valid binding"
            }

        return parsed

    def extract_doc_targets(code_info):

        semantic = code_info.get("semantic_graph", [])
        calls = code_info.get("call_graph", [])
        code_map = code_info.get("code_map", [])

        targets = {
            "api": [],
            "classes": [],
            "services": [],
            "cli": [],
            "flows": [],
            "core_functions": []
        }

        for node in semantic:

            name = node.get("name", "").lower()
            typ = node.get("type", "").lower()

            if "route" in typ or "endpoint" in typ:
                targets["api"].append(node)

            elif "class" in typ:
                targets["classes"].append(node)

            elif "service" in name:
                targets["services"].append(node)

            elif "command" in name or "cli" in name:
                targets["cli"].append(node)

            elif "function" in typ:
                targets["core_functions"].append(node)

        # flow importanti
        for edge in calls[:30]:
            targets["flows"].append(edge)

        return targets

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(
            files_dict=files_dict,
            max_lines=80
        )

        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config"]
        }

        files_b64 = to_b64(relevant_files)

        prompt = f"""
            You are a senior software architect performing deep reverse engineering.

            You must extract BOTH:
            1. SYSTEM ARCHITECTURE (high level)
            2. CODE STRUCTURE + SEMANTIC MODEL (low level)

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            --------------------------------------------------
            INPUT FILES
            --------------------------------------------------
            FILES_B64:
            {files_b64}

            --------------------------------------------------
            TASK
            --------------------------------------------------

            Analyze the codebase and extract:

            ## 1. ARCHITECTURE LAYER
            - architecture_style
            - architectural_patterns
            - major_components
            - modules
            - layering
            - coupling_level
            - cohesion_level
            - entry_points
            - dependency_direction

            ## 2. CODE STRUCTURE LAYER (IMPORTANT)
            For each file, extract:

            - file path
            - classes
            - functions
            - methods
            - imports
            - responsibilities

            ## 3. SEMANTIC FUNCTION GRAPH (CRITICAL)
            For each function:

            - name
            - file
            - inputs
            - outputs
            - purpose
            - calls (internal dependencies)
            - side effects (db, api, io)
            - role (api handler, service, utility, etc.)

            ## 4. CALL RELATIONSHIPS
            Extract function-to-function relationships:
            - caller → callee graph edges

            --------------------------------------------------
            OUTPUT FORMAT (STRICT JSON)
            --------------------------------------------------

            {{
            "architecture": {{
                "architecture_style": "",
                "architectural_patterns": [],
                "major_components": [],
                "modules": [],
                "layering": [],
                "coupling_level": "",
                "cohesion_level": "",
                "entry_points": [],
                "dependency_direction": ""
            }},

            "code_map": [
                {{
                "path": "",
                "classes": [
                    {{
                    "name": "",
                    "methods": []
                    }}
                ],
                "functions": [],
                "imports": [],
                "responsibility": ""
                }}
            ],

            "semantic_graph": [
                {{
                "function": "",
                "file": "",
                "inputs": [],
                "outputs": [],
                "purpose": "",
                "calls": [],
                "side_effects": [],
                "role": ""
                }}
            ],

            "call_graph": [
                {{
                "from": "",
                "to": ""
                }}
            ]
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            --------------------------------------------------
            RULES
            --------------------------------------------------

            - Do NOT hallucinate functions that do not exist
            - Prefer explicit code evidence over inference
            - If uncertain, mark field as "unknown"
            - Keep structure consistent across files
            """

        result = llm_run(prompt, max_tokens=3000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed



class APIAnalyzer(Agent):

    def __init__(self):
        super().__init__(
            "APIAnalyzer",
            depends_on=["CodeArchitectureAnalyzer"]
        )

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(
            files_dict=files_dict, max_lines=None
        )  # max_lines=None per prendere tutto

        source_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] == "source" and f.get("confidence", 0) > 0.6
        }

        # 2. Integrare eventuali info dal contesto (moduli, namespaces, entry points)
        architecture_info = crew_context.get("CodeArchitectureAnalyzer", {})
        extra_info = {
            "modules": architecture_info.get("modules", []),
            "namespaces": architecture_info.get("namespaces", [])
        }

        files_b64 = to_b64(source_files)

        # 3. Prompt ottimizzato per estrazione API con input/output
        prompt = f"""
        You are a senior software architect and API reverse engineering LLM.

        You are given:

        - SOURCE FILES (base64): {files_b64}
        - PROJECT CONTEXT: {json.dumps(project_context, indent=2)}
        - CONTEXT INFO: {json.dumps(extra_info, indent=2)}

        Detect and categorize APIs, including detailed characterization of inputs and outputs:

        - internal APIs
        - public APIs
        - REST endpoints (paths, HTTP methods, input/output schema)
        - CLI commands (arguments, options, output)
        - RPC interfaces (method names, parameters, return types)
        - modules exposing APIs
        - namespaces involved
        - input/output parameters for all APIs
        - protocols, formats, serialization (JSON, XML, etc.)
        - expected errors and status codes

        Return STRICT JSON:

        {{
            "internal_apis":[],
            "public_apis":[],
            "rest_endpoints":[],
            "cli_commands":[],
            "rpc_interfaces":[],
            "api_modules":[],
            "api_namespaces":[],
            "api_io_characterization": []
        }}
        
        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class UsageAnalyzer(Agent):
    """
    Analizza i casi d'uso principali del progetto.
    Integra informazioni API, architettura, directory e dipendenze.
    """

    def __init__(self):
        super().__init__("UsageAnalyzer", depends_on=["APIAnalyzer", "CodeArchitectureAnalyzer", "ProjectTreeAnalyzer", "DependencyDetector", "BuildSystemDetector"])

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Seleziona solo file rilevanti: source e config ad alta confidenza
        logger.info(f"[{self.name}] start running")
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=None)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config"] and f.get("confidence", 0) > 0.6
        }

        # 2. Integra informazioni dai principali agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        architecture_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        dependency_info = self.get_agent_output(crew_context, "DependencyDetector")
        build_info = self.get_agent_output(crew_context, "BuildSystemDetector")

        # 3. Prepara i dati da passare al LLM
        input_payload = {
            "files_b64": to_b64(relevant_files),
            "api_info": api_info,
            "architecture_info": architecture_info,
            "project_tree": project_tree,
            "dependency_info": dependency_info,
            "build_info": build_info
        }

        # 4. Prompt ottimizzato
        prompt = f"""
        You are a senior software architect and system analyst.

        Given the following project information:

        PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

        FILES (source and config, base64):
        {input_payload['files_b64']}

        API INFO:
        {json.dumps(input_payload['api_info'], indent=2)}

        ARCHITECTURE INFO:
        {json.dumps(input_payload['architecture_info'], indent=2)}

        PROJECT TREE:
        {json.dumps(input_payload['project_tree'], indent=2)}

        DEPENDENCIES:
        {json.dumps(input_payload['dependency_info'], indent=2)}

        BUILD INFO:
        {json.dumps(input_payload['build_info'], indent=2)}

        Infer the main use cases, including:

        - use case names
        - actors
        - roles
        - workflows
        - features
        - APIs used per use case
        - namespaces involved

        Return STRICT JSON:

        {{
            "use_cases":[
                {{
                    "name":"",
                    "actors":[],
                    "roles":[],
                    "features":[],
                    "apis":[],
                    "namespaces":[]
                }}
            ]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class SecurityPermissionAnalyzer(Agent):
    """
    Analizza sicurezza, permessi e modelli di autenticazione/autorizzazione.
    Integra informazioni di API, architettura e moduli.
    """

    def __init__(self):
        super().__init__("SecurityPermissionAnalyzer", depends_on=["APIAnalyzer", "CodeArchitectureAnalyzer", "ProjectTreeAnalyzer"])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "script"] and f.get("confidence", 0) > 0.6
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        # 2. Integra info da altri agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        architecture_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")

        prompt = f"""
        You are a security architecture analyst.

        Given the relevant project files (base64), API info, and architecture context:

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        FILES_B64:
        {files_b64}

        API_INFO:
        {json.dumps(api_info, indent=2)}

        ARCHITECTURE_INFO:
        {json.dumps(architecture_info, indent=2)}

        PROJECT_TREE:
        {json.dumps(project_tree, indent=2)}

        Detect and detail:

        - authentication methods (per module/namespace)
        - authorization models and permission levels
        - user roles and admin capabilities
        - sensitive operations
        - security mechanisms
        - secrets, keys, and credentials management

        Return STRICT JSON:

        {{
            "authentication_methods":[],
            "authorization_model":"",
            "user_roles":[],
            "admin_capabilities":[],
            "permission_model":"",
            "security_features":[],
            "secrets_management":[]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=1600)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class DevOpsAnalyzer(Agent):
    """
    Analizza pipeline CI/CD, strategie di deploy e containerizzazione.
    Integra informazioni da build, dependency e project tree.
    """

    def __init__(self):
        super().__init__("DevOpsAnalyzer", depends_on=["BuildSystemDetector", "DependencyDetector", "ProjectTreeAnalyzer"])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["build", "config", "script"] and f.get("confidence", 0) > 0.6
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        # 2. Integra info da altri agenti
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        dependency_info = self.get_agent_output(crew_context, "DependencyDetector")
        build_info = self.get_agent_output(crew_context, "BuildSystemDetector")

        prompt = f"""
        You are a DevOps and infrastructure analyst.

        Given the project files (base64), build info, dependencies, and project tree:

        PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

        FILES_B64:
        {files_b64}

        BUILD_INFO:
        {json.dumps(build_info, indent=2)}

        DEPENDENCY_INFO:
        {json.dumps(dependency_info, indent=2)}

        PROJECT_TREE:
        {json.dumps(project_tree, indent=2)}

        Detect and detail:

        - CI/CD systems and pipelines
        - deployment strategies (per environment)
        - packaging approaches
        - containerization and orchestration (Docker, Kubernetes)
        - automated releases and scripts
        - cross-platform support
        - potential bottlenecks or risks

        Return STRICT JSON:

        {{
            "ci_systems":[],
            "cd_systems":[],
            "deployment_targets":[],
            "containerization":[],
            "orchestration":[],
            "packaging_strategies":[],
            "release_automation":[]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=1600)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed





class VersioningAnalyzer(Agent):
    """
    Analizza il versioning del software e tiene traccia delle entità per versione:
    - features, APIs, namespaces, roles, actors, usecases
    - change, bug, fix
    - timestamp e release history
    """

    def __init__(self):
        super().__init__(
            "VersioningAnalyzer",
            depends_on=[
                "APIAnalyzer",
                "ProjectTreeAnalyzer",
                "SecurityPermissionAnalyzer",
                "DevOpsAnalyzer"
            ]
        )

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=100)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "changelog", "script"] and f.get("confidence", 0) > 0.6
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        # Integra informazioni dagli altri agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        security_info = self.get_agent_output(crew_context, "SecurityAnalyzer")
        devops_info = self.get_agent_output(crew_context, "DevOpsAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")

        prompt = f"""
        You are a software versioning and release historian.

        Given the project files (base64), APIs, features, project tree, security, and DevOps context:

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        FILES_B64:
        {files_b64}

        API_INFO:
        {json.dumps(api_info, indent=2)}

        PROJECT_TREE:
        {json.dumps(project_tree, indent=2)}

        SECURITY_INFO:
        {json.dumps(security_info, indent=2)}

        DEVOPS_INFO:
        {json.dumps(devops_info, indent=2)}

        Detect and produce a structured timeline including:

        - version releases with timestamp
        - for each version:
            - APIs, namespaces, features, roles, actors, usecases
            - for each entity, include 'introduced_in_version' and 'last_modified_version'
        - all changes, bug reports, fixes with timestamps
        - link each change/bug/fix to affected APIs, namespaces, features, roles, actors, usecases, indicating the version for each
        - version control system, semantic versioning, changelog, release notes
        - git workflow, pull request templates, issue templates

        Return STRICT JSON:

        {{
            "versioning_system":"",
            "semantic_versioning":true,
            "git_workflow":"",
            "changelog_present":true,
            "release_notes_present":true,
            "pull_request_templates":true,
            "issue_templates":true,
            "versions":[
                {{
                    "version":"",
                    "release_date":"",
                    "apis":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "namespaces":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "features":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "roles":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "actors":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "usecases":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "changes":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ],
                    "bugs":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ],
                    "fixes":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ]
                }}
            ]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=3000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class DocumentationAnalyzer(Agent):
    """
    Advanced Documentation Analyzer (format-agnostic):
    - Identifica tutti i file documentali (Markdown, PDF, DOCX, XLSX, immagini, diagrammi)
    - Analizza struttura, root e collegamenti tra documenti
    - Rileva strumenti di documentazione e automazione
    - Collega documentazione alle entità di progetto (API, features, roles, actors, usecases)
    - Deduce qualità, completezza, aggiornamento e integrazione
    """

    def __init__(self):
        super().__init__(
            "DocumentationAnalyzer",
            depends_on=[
                "APIAnalyzer",
                "VersioningAnalyzer",
                "SecurityPermissionAnalyzer",
                "DevOpsAnalyzer"
            ]
        )

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_catalog = [
            {"path": path, "type": path.split('.')[-1] if '.' in path else 'unknown', "size": len(content)}
            for path, content in files_dict.items()
        ]

        context_data = {
            "API_INFO": self.get_agent_output(crew_context, "APIAnalyzer"),
            "VERSIONING_INFO": self.get_agent_output(crew_context, "VersioningAnalyzer"),
            "SECURITY_INFO": self.get_agent_output(crew_context, "SecurityPermissionAnalyzer"),
            "DEVOPS_INFO": self.get_agent_output(crew_context, "DevOpsAnalyzer")
        }

        prompt = f"""
        You are an expert documentation engineer. Analyze the project structure and provide a structural JSON report.

        PROJECT CONTEXT: {json.dumps(project_context)}
        FILE CATALOG: {json.dumps(file_catalog)}
        DEPENDENCIES AND ARCHITECTURE: {json.dumps(context_data)}

        TASKS:
        1. Classify files in documentation vs other resources.
        2. Detect tools, readmes, and gaps.
        3. Map files to APIs, roles, and usecases.
        
        STRICT RULES:
        - Return ONLY raw JSON. No markdown backticks (```json).
        - If the file list is large, group files by directory/category instead of listing every single file to stay within token limits.
        - Ensure all JSON fields from the schema are filled.

        SCHEMA:
        {{
            "documentation_present": true,
            "root_documentation_file": "path/to/file",
            "documentation_files": [{{ "path": "...", "type": "...", "completeness": "full/partial/missing", "categories": [] }}],
            "documentation_tools_detected": [{{ "name": "...", "integration_ci_cd": true }}],
            "readme_present": true,
            "faq_present": false,
            "developer_guides": [],
            "api_documentation": [],
            "official_links": [],
            "contacts": null,
            "other_resources": [{{ "path": "...", "type": "..." }}]
        }}
        """

        # Usiamo llm_run_safe invece di llm_run semplice.
        # Questo abiliterà il chunking automatico se la risposta eccede il limite.
        result = llm_run_safe(
            prompt, 
            max_tokens=4000, 
            expect_json=True
        )

        if not result.ok:
            logger.error(f"[{self.name}] LLM failed: {result.error}")
            return {"error": "llm_failed", "raw": result.error}
        
        logger.info(f"[{self.name}] result: {result.data}")
        logger.info(f"[{self.name}] end running")
        return result.data
    


    
class QualityAnalyzer(Agent):
    """
    Analizza il progetto software e produce metriche quantitative per codice, test, sicurezza,
    performance, documentazione, servizio, scalabilità, affidabilità e technical debt.

    Integra informazioni dagli altri agenti:
    - ProjectTreeAnalyzer
    - LanguageDetector
    - BuildSystemDetector
    - DependencyDetector
    - CodeArchitectureAnalyzer
    - APIAnalyzer
    - UsageAnalyzer
    - SecurityPermissionAnalyzer
    - DevOpsAnalyzer
    - DocumentationAnalyzer
    - VersioningAnalyzer
    """

    def __init__(self):
        super().__init__("QualityAnalyzer", depends_on=[
            "ProjectTreeAnalyzer",
            "LanguageDetector",
            "BuildSystemDetector",
            "DependencyDetector",
            "CodeArchitectureAnalyzer",
            "APIAnalyzer",
            "UsageAnalyzer",
            "SecurityPermissionAnalyzer",
            "DevOpsAnalyzer",
            "DocumentationAnalyzer",
            "VersioningAnalyzer"
        ])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # ----------------------------
        # 1. Filtraggio file rilevanti
        # ----------------------------

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)
        relevant_files = {
            f["path"]: files_dict[f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "script"]
        }
        files_b64 = to_b64(relevant_files)

        # ----------------------------
        # 2. Raccolta informazioni dagli altri agenti
        # ----------------------------
        context_info = {agent: self.get_agent_output(crew_context, agent) for agent in self.depends_on}

        # ----------------------------
        # 3. Prompt LLM per analisi avanzata quantitativa
        # ----------------------------
        prompt = f"""
        You are an expert software quality and metrics analyst.

        Analyze the software project in depth using the given files (base64) and context info
        from other agents.

        FILES_B64:
        {files_b64}

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        CONTEXT_INFO:
        {json.dumps(context_info, indent=2)}

        For the project, generate quantitative and qualitative metrics across these dimensions:

        1. CODE QUALITY:
           - maintainability (score 0-10)
           - cohesion and coupling (score 0-10)
           - code complexity per module (cyclomatic complexity, function/method size)
           - coding standard adherence (%)
           - potential bugs and code smells (list + severity)
           - multi-language consistency

        2. TEST QUALITY:
           - test coverage per module (%)
           - completeness of unit, integration, and e2e tests
           - gaps or missing test scenarios
           - reliability of test executions

        3. DOCUMENTATION QUALITY:
           - completeness, clarity, and consistency
           - traceability to APIs, modules, use cases
           - presence of documentation automation tools (Doxygen, Sphinx, MkDocs, etc.)
           - type and structure of documentation (PDF, DOCX, Markdown, HTML, images)

        4. SECURITY:
           - coverage of authentication/authorization
           - secrets, keys, credentials management
           - known vulnerability patterns
           - security score 0-10

        5. PERFORMANCE & SCALABILITY:
           - estimated efficiency of code
           - potential bottlenecks
           - scalability potential
           - parallelization, caching, database access
           - performance score 0-10

        6. SERVICE & RELIABILITY:
           - CI/CD pipeline quality
           - deployment robustness
           - monitoring and logging completeness
           - fault tolerance, availability, disaster recovery
           - reliability score 0-10

        7. DEPENDENCIES & DEVOPS:
           - dependency management quality
           - versioning hygiene
           - containerization/orchestration quality
           - deployment and environment risks

        8. TECHNICAL DEBT & RISKS:
           - estimated technical debt (score 0-10)
           - risk assessment (low/medium/high)
           - traceability of features, APIs, modules, versions, use cases
           - criticality mapping

        Return STRICT JSON with these fields:

        {{
            "code_quality": {{"score":0, "metrics":{{}}, "potential_bugs":[]}},
            "test_quality": {{"coverage":0, "gaps":[], "reliability_score":0}},
            "documentation_quality": {{"score":0, "tools":[],"formats":[],"traceability":{{}}}},
            "security_quality": {{"score":0, "issues":[]}},
            "performance_quality": {{"score":0, "bottlenecks":[], "scalability_score":0}},
            "service_quality": {{"score":0, "ci_cd_score":0, "monitoring":[], "availability_score":0}},
            "technical_debt": {{"score":0, "critical_modules":[]}},
            "risk_level": "",
            "traceability": {{}}
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        # ----------------------------
        # 4. Esecuzione LLM
        # ----------------------------
        result = llm_run(prompt, max_tokens=3500)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        # ----------------------------
        # 5. Salvataggio nel contesto
        # ----------------------------
        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class ProjectMetadataAnalyzer(Agent):
    """
    Analizza tutti i dati prodotti dagli altri agenti e genera un metadata esaustivo del progetto,
    integrando info su linguaggi, dipendenze, architettura, API, uso, sicurezza, DevOps, 
    documentazione, versioning e qualità.
    """

    def __init__(self):
        super().__init__(
            "ProjectMetadataAnalyzer",
            depends_on=[
                "LanguageDetector",
                "DependencyDetector",
                "CodeArchitectureAnalyzer",
                "APIAnalyzer",
                "UsageAnalyzer",
                "DevOpsAnalyzer",
                "SecurityPermissionAnalyzer",
                "DocumentationAnalyzer",
                "VersioningAnalyzer",
                "QualityAnalyzer",
                "ProjectTreeAnalyzer",
                "BuildSystemDetector"
            ]
        )

    def run(self, task, crew_context):
        # Costruzione del contesto completo
        logger.info(f"[{self.name}] start running")
        context_info = {agent: self.get_agent_output(crew_context, agent) for agent in self.depends_on}
        project_context = self.get_task(task, "project_context", {})

        prompt = f"""
        You are a senior software project analyst and documentation generator.

        Using the full context of previous analyses, generate a comprehensive project metadata report.

        PROJECT_CONTEXT:

        {json.dumps(project_context, indent=2)}

        CONTEXT_INFO:
        
        {json.dumps(context_info, indent=2)}

        Infer:

        - project_description
        - goal
        - targets
        - benefits
        - risks
        - techstack
        - architecture_summary
        - features
        - settings
        - APIs
        - namespaces
        - modules
        - entry_points
        - directory_structure
        - build_systems
        - ci_cd
        - containerization
        - deployment_targets
        - security_summary
        - authentication_methods
        - authorization_models
        - user_roles
        - admin_capabilities
        - sensitive_operations
        - secrets_management
        - documentation_summary
        - documentation_tools
        - documentation_coverage
        - versioning_summary
        - release_history
        - changelog
        - technical_debt
        - code_quality
        - test_quality
        - performance_quality
        - service_quality
        - risk_level
        - traceability

        Return STRICT JSON with all fields populated. Use null if unknown.

        {{
            "project_description":"",
            "goal":"",
            "targets":[],
            "benefits":[],
            "risks":[],
            "techstack":[],
            "architecture_summary":"",
            "features":[],
            "settings":[],
            "apis":[],
            "namespaces":[],
            "modules":[],
            "entry_points":[],
            "directory_structure":{{}},
            "build_systems":[],
            "ci_cd":[],
            "containerization":[],
            "deployment_targets":[],
            "security_summary":{{}},
            "authentication_methods":[],
            "authorization_models":[],
            "user_roles":[],
            "admin_capabilities":[],
            "sensitive_operations":[],
            "secrets_management":[],
            "documentation_summary":{{}},
            "documentation_tools":[],
            "documentation_coverage":{{}},
            "versioning_summary":{{}},
            "release_history":[],
            "changelog_present":true,
            "technical_debt":{{}},
            "code_quality":{{}},
            "test_quality":{{}},
            "performance_quality":{{}},
            "service_quality":{{}},
            "risk_level":"",
            "traceability":{{}}
        }}
        
        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=4000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed



class MarkdownElementExtractor:

    def __init__(self):
        self.heading_re = re.compile(r'^\s*(#{1,6})\s+(.+)$')
        self.image_re = re.compile(r'!\[(.*?)\]\((.*?)\)')
        self.link_re = re.compile(r'\[(.*?)\]\((.*?)\)')
        self.code_block_re = re.compile(r'```(\w+)?\s*\n([\s\S]*?)```', re.DOTALL)
        self.table_re = re.compile(r'(\|.*\|(\n\|.*\|)+)', re.MULTILINE)

    def build_heading_tree(self, headings):

        root = []
        stack = []

        headings = sorted(headings, key=lambda x: x.get("line", 0))

        for h in headings:
            node = {
                "id": h["id"],
                "level": h["level"],
                "title": h["title"],
                "line": h["line"],
                "end_line": h["end_line"],
                "children": [],
                "file_path": h["file_path"],
                "parent_id": None
            }

            while stack and stack[-1]["level"] >= node["level"]:
                stack.pop()

            if not stack:
                root.append(node)
            else:
                node["parent_id"] = stack[-1].get("id")
                stack[-1]["children"].append(node)

            stack.append(node)

        return root


    def _parse_table(self, rows):

        clean = []

        for r in rows:
            if set(r.replace("|", "").replace(":", "").strip()) <= {"-"}:
                continue

            cells = [c.strip() for c in r.split("|") if c.strip()]
            if cells:
                clean.append(cells)

        if not clean:
            return None

        return {
            "header": clean[0],
            "rows": clean[1:]
        }

    def parse(self, markdown: str, file_path: str) -> Dict[str, Any]:

        lines = markdown.split("\n")
        headings = self.extract_headings(lines, file_path)
        tree = self.build_heading_tree(headings)

        return {
            "headings": headings,
            "heading_tree": tree,
            "images": self.extract_images(markdown),
            "links": self.extract_links(markdown),
            "code_blocks": self.extract_code_blocks(markdown),
            "tables": self.extract_tables(markdown),
            "sections": self.build_sections_from_tree(tree, lines),
            "raw_text": markdown
        }



    def make_id(self, file_path: str, line: int, title: str) -> str:
        raw = f"{file_path.strip().lower()}|{line}|{title.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    # -------------------------------------------------
    # HEADINGS (H1-H6)
    # -------------------------------------------------
    def extract_headings(self, lines, file_path: str):

        headings = []

        for i, line in enumerate(lines):
            match = self.heading_re.match(line.strip())

            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                
                headings.append({
                    "id": self.make_id(file_path, i, text),
                    "level": level,
                    "title": text,
                    "line": i,
                    "end_line": None,
                    "file_path": file_path
                })

        
        for i in range(len(headings)):
            start = headings[i]["line"]

            end = len(lines)

            for j in range(i + 1, len(headings)):
                if headings[j]["level"] <= headings[i]["level"]:
                    end = headings[j]["line"]
                    break

            headings[i]["end_line"] = end

        return headings

    # -------------------------------------------------
    # IMAGES
    # -------------------------------------------------
    def extract_images(self, markdown: str) -> List[Dict]:
        return [
            {
                "alt": match.group(1),
                "path": match.group(2)
            }
            for match in self.image_re.finditer(markdown)
        ]

    # -------------------------------------------------
    # LINKS
    # -------------------------------------------------
    def extract_links(self, markdown: str) -> List[Dict]:
        return [
            {
                "text": match.group(1),
                "url": match.group(2)
            }
            for match in self.link_re.finditer(markdown)
        ]

    # -------------------------------------------------
    # CODE BLOCKS
    # -------------------------------------------------
    def extract_code_blocks(self, markdown: str) -> List[Dict]:
        blocks = []

        for match in self.code_block_re.finditer(markdown):
            language = match.group(1) or "unknown"
            code = match.group(2)

            blocks.append({
                "language": language,
                "code": code.strip()
            })

        return blocks

    def build_sections_from_tree(self, tree, lines):

        sections = []
        visited = set()

        def walk(node):

            if node["id"] in visited:
                return
            visited.add(node["id"])

            start = node["line"]
            end = node.get("end_line", len(lines))

            sections.append({
                "id": node["id"],
                "name": node["title"],
                "level": node["level"],
                "file_path": node.get("file_path"),
                "parent_id": node.get("parent_id"),
                "content": "\n".join(lines[start:end])
            })

            for child in node.get("children", []):
                walk(child)

        for root in tree:
            walk(root)

        return sections

    # -------------------------------------------------
    # TABLES (basic markdown table detection)
    # -------------------------------------------------
    def extract_tables(self, markdown: str):

        lines = markdown.split("\n")
        tables = []
        current = []

        for line in lines:
            if "|" in line and line.count("|") >= 2:
                current.append(line)
            else:
                if len(current) > 1:
                    table = self._parse_table(current)
                    if table:
                        tables.append(table)
                current = []

        if len(current) > 1:
            table = self._parse_table(current)
            if table:
                tables.append(table)

        return tables

class MDTemplateAnalyzer(Agent):

    def __init__(self):
        super().__init__("MDTemplateAnalyzer", depends_on=[
                "LanguageDetector",
                "DependencyDetector",
                "CodeArchitectureAnalyzer",
                "APIAnalyzer",
                "UsageAnalyzer",
                "DevOpsAnalyzer",
                "SecurityPermissionAnalyzer",
                "DocumentationAnalyzer",
                "VersioningAnalyzer",
                "QualityAnalyzer",
                "ProjectTreeAnalyzer",
                "BuildSystemDetector",
                "ProjectMetadataAnalyzer"
            ])

        with open("./md-template.json", "r", encoding="utf-8") as f:
            self.base_template = json.load(f)

    def run(self, task: dict, crew_context: dict):
        
        logger.info(f"[{self.name}] start running")

        github_token = self.get_task(task, "github_token", "")
        github_username = self.get_task(task, "github_username", "")
        

        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # -------------------------------------------------
        # 1. GitHub Manager
        # -------------------------------------------------
        gh = GitHubManager(
            github_token=github_token,
            username=github_username
        )

        # -------------------------------------------------
        # 2. Repo passate da input / altri agenti
        # -------------------------------------------------
        input_repos = self.get_task(task, "repos", [])

        logger.info(f"[{self.name}] input repos: {len(input_repos)}")
        logger.info(json.dumps(input_repos, indent=2))

        # -------------------------------------------------
        # 3. Repo trovate automaticamente simili al progetto
        # -------------------------------------------------
        discovered_repos = []

        try:
            discovered_repos = gh.discover_repos_from_context(
                crew_context,
                max_repos=1
            )

            logger.info(
                f"[{self.name}] auto discovered repos: {len(discovered_repos)}"
            )
            logger.info(json.dumps(discovered_repos, indent=2))

        except Exception as e:
            logger.warning(
                f"[{self.name}] discover_repos_from_context failed: {e}"
            )

        # -------------------------------------------------
        # 4. Repo user personali (opzionale)
        # -------------------------------------------------
        user_repos = []

        try:
            if github_username:
                user_repos = gh.get_user_repos(max_repos=1)

                logger.info(
                    f"[{self.name}] user repos found: {len(user_repos)}"
                )
                logger.info(json.dumps(user_repos, indent=2))

        except Exception as e:
            logger.warning(
                f"[{self.name}] get_user_repos failed: {e}"
            )

        # -------------------------------------------------
        # 5. Merge intelligente finale
        # -------------------------------------------------
        repos = GitHubManager.merge_repos(
            input_repos,
            discovered_repos,
            user_repos,
            max_total=8
        )

        logger.info(
            f"[{self.name}] final repos to analyze: {len(repos)}"
        )
        logger.info(json.dumps(repos, indent=2))

        # Salva per debug nel context
        crew_context["repos"] = repos

        # -------------------------------------------------
        # 6. Recupera dati progetto
        # -------------------------------------------------
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        language_info = self.get_agent_output(crew_context, "LanguageDetector")
        build_info = self.get_agent_output(crew_context, "BuildSystemDetector")
        usage_info = self.get_agent_output(crew_context, "UsageAnalyzer")
        
        # Estraiamo i grafi e le mappe direttamente dal dizionario di CodeArchitectureAnalyzer
        code_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        code_graph = code_info.get("semantic_graph", [])
        call_graph = code_info.get("call_graph", [])
        code_map = code_info.get("code_map", [])
        doc_targets = CodeArchitectureAnalyzer.extract_doc_targets(code_info)
        
        quality_info = self.get_agent_output(crew_context, "QualityAnalyzer")

        

        # -------------------------------------------------
        # 7. Analizza repo markdown (STRUTTURALE + AST)
        # -------------------------------------------------
        extractor = MarkdownElementExtractor()
        repo_structures = {}

        for repo_info in repos:

            owner = repo_info["owner"]
            repo = repo_info["repo"]

            logger.info(f"\n[{self.name}] analyzing repo: {owner}/{repo}")

            try:
                md_files = gh.fetch_repo_md_files(
                    owner=owner,
                    repo=repo
                )

                logger.info(f"[{self.name}] markdown files found: {len(md_files)}")

                parsed_files = {}

                # -------------------------------------------------
                # 1. PARSING COMPLETO DI OGNI FILE MD
                # -------------------------------------------------
                for path, content in md_files.items():
                    parsed_files[path] = extractor.parse(content, file_path=path)

                repo_ast = {
                    "files": parsed_files,
                    "global_headings": [],
                    "global_tables": [],
                    "global_links": [],
                    "global_images": [],
                    "global_code_blocks": []
                }

                for file_path, file_data in parsed_files.items():
                    repo_ast["global_headings"].extend(file_data.get("headings", []))
                    repo_ast["global_tables"].extend(file_data.get("tables", []))
                    repo_ast["global_links"].extend(file_data.get("links", []))
                    repo_ast["global_images"].extend(file_data.get("images", []))
                    repo_ast["global_code_blocks"].extend(file_data.get("code_blocks", []))

                section_code_index = []

                for file_path, parsed in parsed_files.items():

                    for section in parsed.get("headings", []):

                        section_name = section["title"]
                        section_level = section.get("level", 1)
                        section_line = section.get("line", 0)

                        binding = CodeArchitectureAnalyzer.find_relevant_code(
                            section_name,
                            repo_ast,
                            {
                                "semantic_graph": code_graph,
                                "call_graph": call_graph,
                                "code_map": code_map
                            }
                        )

                        clean_binding = json.loads(json.dumps(binding, default=str))
                        section["code_scope"] = clean_binding
                        section["binding"] = clean_binding

                        section_code_index.append({
                            "section": section_name,
                            "file": file_path,
                            "level": section_level,
                            "line": section_line,
                            "binding": binding,
                            "parent": None,
                            "depth": section_level
                        })

                code_section_index = {}

                for entry in section_code_index:
                    binding = entry["binding"]

                    # parent NON lo calcoli qui, lo prendi dal parser
                    entry["parent"] = None  # default
                    
                    for func in binding.get("functions", []):
                        code_section_index.setdefault(func, []).append(entry["section"])

                    for clss in binding.get("classes", []):
                        code_section_index.setdefault(clss, []).append(entry["section"])

                # -------------------------------------------------
                # 2. AGGREGAZIONE STRUTTURALE (IMPORTANTE)
                # -------------------------------------------------
                repo_ast["section_code_index"] = section_code_index
                repo_ast["code_section_index"] = code_section_index

                # -------------------------------------------------
                # 3. LLM SOLO PER STRUTTURA (NON PARSING)
                # -------------------------------------------------
                prompt = f"""
                You are an expert in documentation architecture.

                You are given a FULL MARKDOWN AST.

                TASK:
                - detect documentation patterns
                - infer structure hierarchy
                - identify missing sections
                - propose ideal template structure

                DO NOT parse markdown.

                Return ONLY JSON:

                {{
                    "repo": "{owner}/{repo}",
                    "structure_summary": {{
                        "has_readme": true,
                        "has_api_docs": true,
                        "has_examples": true,
                        "depth_analysis": "low|medium|high",
                        "documentation_quality": "low|medium|high"
                    }},
                    "patterns": [],
                    "insights": []
                }}

                INPUT AST:
                {json.dumps(repo_ast, indent=2)}
                """

                result = llm_run(prompt, max_tokens=3500)
                analysis_json = extract_json(result)

                if analysis_json:
                    repo_structures[f"{owner}/{repo}"] = {
                        "ast": repo_ast,
                        "analysis": analysis_json
                    }

                    logger.info(f"[{self.name}] Parsed OK: {owner}/{repo}")

                else:
                    logger.warning(f"[{self.name}] Invalid JSON: {owner}/{repo}")

            except Exception as e:
                logger.warning(f"[{self.name}] Repo failed {owner}/{repo}: {e}")

        # -------------------------------------------------
        # 8. Prompt finale
        # -------------------------------------------------
        logger.info(f"\n[{self.name}] Building FINAL template...\n")

        prompt_template = """
            You are a Principal Software Documentation Architect.

            Your task is NOT to write documentation.

            Your task is to DESIGN the COMPLETE DOCUMENTATION STRUCTURE
            for a NEW software project.

            The final output must be a JSON document compatible with md-template.json.

            =========================================================
            IMPORTANT CONCEPT
            =========================================================

            The analyzed repositories are NOT templates to copy.

            The analyzed repositories represent:

            - documentation patterns
            - documentation strategies
            - documentation organization styles
            - file grouping approaches
            - section hierarchies
            - documentation best practices

            You MUST learn from them.

            You MUST NOT reproduce them.

            You MUST create a NEW documentation architecture specifically
            tailored to the software being analyzed.

            =========================================================
            INPUT SOURCES
            =========================================================

            1) Base Documentation Template
            (reference only)

            {base_template}

            ---------------------------------------------------------

            2) Documentation Structures Extracted From Real Repositories

            {repo_structures}

            ---------------------------------------------------------

            3) High Level Project Context

            {project_context}

            ---------------------------------------------------------

            4) Project Analysis Produced By Specialized Agents

            Project Tree:
            {project_tree}

            Languages:
            {language_info}

            Build System:
            {build_info}

            Usage Analysis:
            {usage_info}

            Code Architecture:
            {code_info}

            Documentation Targets:
            {doc_targets}

            Quality Analysis:
            {quality_info}

            =========================================================
            PRIMARY OBJECTIVE
            =========================================================

            Design the BEST possible markdown documentation architecture
            for THIS specific project.

            The structure must fit:

            - actual modules
            - actual services
            - actual APIs
            - actual workflows
            - actual deployment model
            - actual architecture
            - actual dependencies
            - actual security model
            - actual user flows

            discovered by the analyzers.

            =========================================================
            REASONING PROCESS
            =========================================================

            STEP 1

            Analyze all repository documentation structures.

            Identify:

            - recurring files
            - recurring sections
            - recurring subsection hierarchies
            - recurring documentation domains
            - recurring navigation models

            ---------------------------------------------------------

            STEP 2

            Analyze the target software.

            Determine:

            - software type
            - architectural complexity
            - deployment complexity
            - API complexity
            - module count
            - service count
            - integration count
            - security complexity
            - operational complexity

            ---------------------------------------------------------

            STEP 3

            Compare repository patterns with project needs.

            For each documentation area decide:

            - KEEP
            - MODIFY
            - REMOVE
            - CREATE NEW

            based on the actual project.

            ---------------------------------------------------------

            STEP 4

            Generate a NEW documentation architecture.

            The final structure must be:

            - project specific
            - analyzer driven
            - repository inspired
            - non copied
            - complete

            =========================================================
            FILE GENERATION RULES
            =========================================================

            For EACH markdown file define:

            - file path
            - purpose
            - sections
            - subsections
            - documentation targets

            Each section must belong to exactly one file.

            Avoid duplication.

            =========================================================
            SECTION GENERATION RULES
            =========================================================

            Sections must be generated from:

            - architecture analysis
            - APIs
            - modules
            - services
            - workflows
            - dependencies
            - deployment
            - security
            - configuration
            - testing
            - usage

            Only include sections that make sense for THIS project.

            Do not blindly reproduce repository structures.

            =========================================================
            DIRECTORY TREE RULES
            =========================================================

            The markdown_directory_tree must represent:

            - actual documentation hierarchy
            - actual navigation hierarchy
            - actual logical grouping

            It may differ from md-template.json if the project
            requires a better structure.

            =========================================================
            OUTPUT FORMAT
            =========================================================

            Return ONLY VALID JSON.

            Schema:

            {
            "documentation_strategy": {
                "documentation_type": "",
                "complexity": "",
                "rationale": ""
            },

            "markdown_directory_tree": {},

            "markdown_files": [
                {
                "path": "",
                "purpose": "",
                "derived_from": [],
                "project_entities": [],
                "sections": [
                    {
                    "title": "",
                    "purpose": "",
                    "source_reasoning": "",
                    "subsections": []
                    }
                ]
                }
            ],

            "coverage_map": {},

            "missing_docs_detected": [],

            "documentation_principles": [],

            "insights": [],

            "doc_targets_used": []
            }

            =========================================================
            CRITICAL RULES
            =========================================================

            DO NOT:

            - copy repository structures
            - copy repository file names blindly
            - copy repository sections blindly
            - replicate md-template.json as-is

            INSTEAD:

            - reason across ALL repositories
            - reason across ALL analyzers
            - reason across ALL project metadata
            - build a NEW documentation architecture

            The final architecture must look as if it had been
            designed manually by a senior documentation architect
            after studying both:

            1) similar projects
            2) the actual target project

            Return ONLY JSON.
            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            """


        prompt_final = prompt_template.format(
            base_template=json.dumps(self.base_template, indent=2, ensure_ascii=False),
            repo_structures=json.dumps(repo_structures, indent=2, ensure_ascii=False),
            project_tree=json.dumps(project_tree, indent=2, ensure_ascii=False),
            language_info=json.dumps(language_info, indent=2, ensure_ascii=False),
            build_info=json.dumps(build_info, indent=2, ensure_ascii=False),
            usage_info=json.dumps(usage_info, indent=2, ensure_ascii=False),
            code_info=json.dumps(code_info, indent=2, ensure_ascii=False),
            doc_targets=json.dumps(doc_targets, indent=2, ensure_ascii=False),
            quality_info=json.dumps(quality_info, indent=2, ensure_ascii=False),
            project_context=json.dumps(project_context, indent=2, ensure_ascii=False),

            output_schema=json.dumps({
                "markdown_directory_tree": {},
                "markdown_files": [],
                "documentation_principles": [],
                "insights": [],
                "missing_docs_detected": [],
                "coverage_map": {},
                "doc_targets_used": []
            })
        )

        result_final = llm_run(prompt_final, max_tokens=5000)
        logger.info(f"\n[{self.name}] Result: {result_final}\n")
        final_structure = extract_json(result_final)
        if not final_structure:
            final_structure = {
                "error": "invalid_json",
                "raw": result_final
            }

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return final_structure




class MDDocumentationMaker(Agent):

    def __init__(self):
        super().__init__(
            "MDDocumentationMaker",
            depends_on=[
                "MDTemplateAnalyzer"
            ]
        )

    # =========================
    # UTILITIES
    # =========================

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_tech_registry(self, tech_registry_path="md-tech.json"):
        data = self.load_json(tech_registry_path)
        return data.get("technologies", {})

    def normalize_text(self, obj):
        try:
            return json.dumps(obj, ensure_ascii=False).lower()
        except:
            return str(obj).lower()

    def extract_words(self, text):
        return set(re.findall(r"[a-zA-Z0-9\+\#\.\-]+", text.lower()))

    # =========================
    # TECH VISUAL EXTRACTION
    # =========================

    def build_visual_assets(self, project_context, tech_registry_path="md-tech.json"):

        tech_registry = self.load_tech_registry(tech_registry_path)

        detected = set()
        text = self.normalize_text(project_context)
        words = self.extract_words(text)

        for slug, meta in tech_registry.items():

            slug_l = slug.lower()
            name_l = meta.get("name", "").lower()
            tags = [t.lower() for t in meta.get("tags", [])]

            if (
                slug_l in text or
                name_l in text or
                slug_l in words or
                name_l in words or
                any(tag in words for tag in tags)
            ):
                detected.add(slug)

        return {
            "detected": sorted(list(detected)),
            "tech_registry": tech_registry
        }
    
    def build_code_reference_index(self, crew_context):
        code = crew_context.get("CodeArchitectureAnalyzer", {})
        api = crew_context.get("APIAnalyzer", {})

        return {
            "files": [f.get("path") for f in code.get("code_map", [])],
            "classes": [
                c.get("name")
                for f in code.get("code_map", [])
                for c in f.get("classes", [])
            ],
            "functions": [
                fn.get("function") or fn.get("name")
                for fn in code.get("semantic_graph", [])
            ],
            "endpoints": api.get("rest_endpoints", [])
        }

    # =========================
    # LLM PROMPT BUILDER
    # =========================

    def build_prompt(self, file_def, template, tech, context, visual_assets):

        return f"""
            You are an expert technical documentation generator.
            Your task is to generate a COMPLETE and VALID markdown documentation file.

                        --------------------------------------------------
                        INPUT CONTEXT
                        --------------------------------------------------

                        FILE PATH:
                        {file_def["path"]}

                        PROJECT CONTEXT:
                        {json.dumps(context, indent=2)}

                        TECH REGISTRY:
                        {json.dumps(tech, indent=2)}

                        DETECTED TECHNOLOGIES:
                        {json.dumps(visual_assets["detected"], indent=2)}

                        TEMPLATE STRUCTURE:
                        {json.dumps(file_def["sections"], indent=2)}

                        --------------------------------------------------
                        CODE INDEX (AUTHORITATIVE SOURCE - DO NOT INVENT)
                        --------------------------------------------------

                        FILES:
                        {json.dumps(context["code_index"]["files"], indent=2)}

                        CLASSES:
                        {json.dumps(context["code_index"]["classes"], indent=2)}

                        FUNCTIONS:
                        {json.dumps(context["code_index"]["functions"], indent=2)}

                        API ENDPOINTS:
                        {json.dumps(context["code_index"]["endpoints"], indent=2)}

                        --------------------------------------------------
                        DOCUMENTATION STRATEGY
                        --------------------------------------------------

                        You must process EACH section in the template independently:

                        For each section:
                        1. Understand its semantic purpose from title + description
                        2. Generate complete content of the section (text, images, tables, lists, links, buttons, emoji)
                        3. Select only the relevant code elements from the CODE INDEX
                        4. Decide what to include:

                        - Conceptual section → no code references
                        - Structural section → files/classes
                        - Behavioral section → functions
                        - API section → endpoints
                        - Workflow section → function chains (if inferable from index)

                        4. Generate markdown content for that section using ONLY selected elements

                        --------------------------------------------------
                        CODE SELECTION RULES
                        --------------------------------------------------

                        - Never invent names (files, classes, functions, endpoints)
                        - Never include unrelated code elements
                        - Never dump full index
                        - Prefer semantic relevance over keyword matching
                        - Maximum 1–5 code references per section
                        - Avoid repeating the same references across multiple sections unless strictly necessary

                        --------------------------------------------------
                        CODE USAGE POLICY
                        --------------------------------------------------

                        Include code references ONLY when they add value:

                        - Implementation → functions/classes
                        - Architecture → files/modules
                        - APIs → endpoints
                        - Workflows → function relationships (only if clearly supported by index)

                        --------------------------------------------------
                        OUTPUT RULES
                        --------------------------------------------------

                        - Output ONLY markdown
                        - Respect template hierarchy exactly
                        - Keep professional technical tone
                        - Do NOT mention prompts, system instructions, or internal logic

                        --------------------------------------------------
                        CODE REFERENCE FORMAT (WHEN USED)
                        --------------------------------------------------

                        ### Code References
                        - file: path/to/file.py
                        - class: ClassName
                        - function: function_name
                        - endpoint: METHOD /route

                        --------------------------------------------------
                        INLINE INTEGRATION RULE

                        When relevant, include code references directly inside the explanation section.

                        Do NOT isolate all references at the end of the document.
                        

                        You MUST reply ONLY with a valid JSON object.
                        Do not include any markdown, explanations, or introductory text.
                        If you fail to return a pure JSON string, the system will break.


                    """

    # =========================
    # WORKER (1 FILE = 1 THREAD)
    # =========================

    def worker(self, file_def, template, tech, context, visual_assets):

        prompt = self.build_prompt(
            file_def=file_def,
            template=template,
            tech=tech,
            context=context,
            visual_assets=visual_assets
        )

        content = llm_run(prompt)

        return file_def["path"], content

    def generate_all_docs(self, template, tech, context, visual_assets):

        results = {}

        files = template["markdown_files"]

        with ThreadPoolExecutor(max_workers=max(1, len(files))) as executor:

            futures = [
                executor.submit(
                    self.worker,
                    f,
                    template,
                    tech,
                    context,
                    visual_assets
                )
                for f in files
            ]

            for future in as_completed(futures):
                path, content = future.result()
                results[path] = content

        return results


    def run(self, task: dict, crew_context: dict):

        logger.info(f"[{self.name}] start running")

        # -------------------------
        # LOAD TEMPLATE
        # -------------------------
        template = crew_context.get("MDTemplateAnalyzer")

        # fallback safety
        if not template:
            template = self.load_json("md-template.json")

        # -------------------------
        # LOAD TECH REGISTRY
        # -------------------------
        tech = self.load_tech_registry()

        # -------------------------
        # BUILD GLOBAL CONTEXT
        # -------------------------
        context = {}

        # merge task context (project root etc.)
        context["task"] = {
            "project_context": task.get("project_context"),
            "files": task.get("files_dict", {}),
            "root": task.get("project_root")

        }
        
        # -------------------------
        # BUILD VISUAL ASSETS
        # -------------------------
        visual_assets = self.build_visual_assets(context)

        logger.info(f"[{self.name}] generating docs in parallel")

        # -------------------------
        # PARALLEL GENERATION
        # -------------------------
        docs = self.generate_all_docs(template, tech, context, visual_assets)

        # -------------------------
        # FINAL STRUCTURE
        # -------------------------
        final_structure = {
            "generated_files": docs,
            "detected_technologies": visual_assets["detected"]
        }

        logger.info(f"[{self.name}] generation complete")

        return final_structure

    

class DoxygenConfigBuilder(Agent):
    """
    Enhanced Doxygen configuration builder with actual Doxygen CLI generation.

    Workflow:
    1. Generates deterministic Doxyfile base using 'doxygen -g'.
    2. Generates base header.html, footer.html, stylesheet.css via Doxygen.
    3. Uses LLM to analyze project (languages, protocols, tools, versions, licenses, Markdown docs)
       and optimize Doxyfile & assets.
    """

    def __init__(self):
        super().__init__(
            "DoxygenConfigBuilder",
            depends_on=[
                "ProjectTreeAnalyzer",
                "LanguageDetector",
                "BuildSystemDetector",
                "DependencyDetector",
                "CodeArchitectureAnalyzer",
                "APIAnalyzer",
                "UsageAnalyzer",
                "DocumentationAnalyzer",
                "MDDocumentationMaker"
            ]
        )

    def generate_doxygen_base(self, project_root: str) -> dict:
        """
        Generate deterministic base Doxyfile, header/footer/css using Doxygen CLI.
        Returns paths and asset content.
        """
        base_dir = os.path.join(project_root, "_doxygen_base")
        os.makedirs(base_dir, exist_ok=True)

        doxyfile_path = os.path.join(base_dir, "Doxyfile")

        # Step 1: Generate Doxyfile base
        subprocess.run(["doxygen", "-g", doxyfile_path], check=True)

        # Step 2: Optionally, generate HTML assets (header/footer/css) via Doxygen
        # Create a minimal config to output HTML assets
        subprocess.run(["doxygen", doxyfile_path], check=True)

        # Read header/footer/css if they exist
        assets = {}
        for name in ["header.html", "footer.html", "stylesheet.css"]:
            path = os.path.join(base_dir, name)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    assets[name] = f.read()
            else:
                assets[name] = ""

        return {"doxyfile_path": doxyfile_path, "assets": assets}

    def run(self, task: dict, crew_context: dict):
        logger.info(f"[{self.name}] start running")
        project_root = task.get("project_root", ".")
        base = self.generate_doxygen_base(project_root)

        with open(base["doxyfile_path"], "r", encoding="utf-8") as f:
            base_doxy = f.read()
        assets = base["assets"]

        files_b64 = to_b64(task.get("files_dict", {}))
        context_json = json.dumps(crew_context, indent=2)

        # ----------------------------
        # LLM OPTIMIZATION
        # ----------------------------
        prompt = f"""
        You are an expert in Doxygen configuration, documentation systems, web UI,
        and technical documentation best practices.

        INPUTS:
        - Base Doxyfile generated by 'doxygen -g':
        {base_doxy}

        - Base HTML assets:
        HEADER: {assets.get("header.html","")}
        FOOTER: {assets.get("footer.html","")}
        CSS: {assets.get("stylesheet.css","")}

        - Project files (Base64): {files_b64}

        - Full project context (languages, frameworks, build system, dependencies,
          protocols, tools, versions, licenses, Markdown docs):
        {context_json}

        TASK:
        Optimize Doxyfile parameters based on project structure, Markdown docs,
        APIs, usage patterns, protocols, tools, licenses, versions.

        Ensure:
        - Markdown integration
        - Call graphs, inheritance diagrams, dependency graphs
        - Correct input paths
        - Output formats consistent with project needs

        RETURN JSON:
        {{
            "Doxyfile": "...",
            "header.html": "...",
            "footer.html": "...",
            "stylesheet.css": "...",
            "config_summary": {{
                "parameters": {{ ... }},
                "main_page": "index.html",
                "has_diagrams": true,
                "optimized_for": "GitHub Pages"
            }}
        }}

        Return ONLY valid JSON.
        """

        result = llm_run(prompt, max_tokens=7000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        # ----------------------------
        # SAVE FILES
        # ----------------------------
        output_dir = os.path.join(project_root, "doxygen_custom")
        os.makedirs(output_dir, exist_ok=True)

        for key in ["Doxyfile", "header.html", "footer.html", "stylesheet.css"]:
            if key in parsed:
                with open(os.path.join(output_dir, key), "w", encoding="utf-8") as f:
                    f.write(parsed[key])

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class DoxygenDocumentationUXBuilder(Agent):
    """
    Advanced Documentation UI/UX Architect using Doxygen data and full project analysis.

    Produces:
    - header.html
    - footer.html
    - stylesheet.css
    - index.html (landing page)
    - Secondary pages: API explorer, architecture, use cases, security, devops, quality, versioning
    - Updates Doxyfile if project analysis suggests optimizations
    - Fills content dynamically based on project data (tech stack, APIs, use cases, roles, diagrams)
    """

    def __init__(self):
        super().__init__(
            "DoxygenDocumentationUXBuilder",
            depends_on=[
                "DoxygenConfigBuilder",
                "ProjectMetadataAnalyzer",
                "MDDocumentationMaker",
                "UsageAnalyzer",
                "APIAnalyzer",
                "SecurityPermissionAnalyzer",
                "DevOpsAnalyzer",
                "VersioningAnalyzer",
                "QualityAnalyzer",
                "DocumentationAnalyzer"
            ]
        )

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):
        logger.info(f"[{self.name}] start running")
        project_root = task.get("project_root", ".")
        doxyfile_path = os.path.join(project_root, "doxygen_custom", "Doxyfile")
        full_context = {k: crew_context.get(k, {}) for k in self.depends_on}
        context_json = json.dumps(full_context, indent=2)

        prompt = f"""
        You are a senior UI/UX architect and documentation engineer.
        Your goal is to generate a **fully populated interactive documentation website**
        based on all available project data.

        INPUTS:
        - Current Doxyfile path: {doxyfile_path}
        - Full project context (languages, toolchain, use cases, roles, protocols,
          versions, licenses, APIs, usage patterns, Markdown files):
        {context_json}

        TASK:
        1) Generate the full HTML documentation site:
           - index.html: hero section (project name, description, logo), badges (build, coverage, license), quick links (GitHub, MD docs)
           - Pages: API, architecture, use cases, security, devops, versioning, quality metrics
           - Navigation: topbar, sidebar, breadcrumbs, search form
           - Populate each page with actual project data, including:
             - Tech stack tables
             - Supported protocols
             - Modules and component relationships
             - Use cases and user roles
             - Internal and external links
             - Code examples from the project
             - Diagrams for architecture, sequence, flow
        2) Ensure visual consistency: modern theme, responsive layout, light/dark mode
        3) Review the existing Doxyfile:
           - Adjust INPUT paths if needed
           - Enable Markdown integration
           - Enable diagrams, call graphs, dependency graphs
           - Suggest any other optimizations
        4) Return updated Doxyfile if modified, and all populated HTML/CSS assets

        OUTPUT JSON:
        {{
            "updated_doxyfile": "...",
            "html_files": [
                {{"path": "header.html", "content": ""}},
                {{"path": "footer.html", "content": ""}},
                {{"path": "stylesheet.css", "content": ""}},
                {{"path": "index.html", "content": ""}},
                {{"path": "pages/api.html", "content": ""}},
                {{"path": "pages/architecture.html", "content": ""}},
                {{"path": "pages/usecases.html", "content": ""}},
                {{"path": "pages/security.html", "content": ""}},
                {{"path": "pages/devops.html", "content": ""}},
                {{"path": "pages/versioning.html", "content": ""}},
                {{"path": "pages/quality.html", "content": ""}}
            ],
            "ui_architecture": {{"pages": [], "navigation": {{}}, "user_flows": []}},
            "components": {{"tables": [], "charts": [], "diagrams": [], "cards": [], "forms": []}},
            "design_system": {{
                "theme": "modern",
                "dark_mode": true,
                "layout": "responsive",
                "typography": "professional"
            }}
        }}

        Return ONLY JSON.
        """

        result = llm_run(prompt, max_tokens=10000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        # SAVE HTML FILES
        output_dir = os.path.join(project_root, "doxygen_ui")
        os.makedirs(output_dir, exist_ok=True)
        for f in parsed.get("html_files", []):
            fpath = os.path.join(output_dir, f["path"])
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as hfile:
                hfile.write(f["content"])

        # UPDATE Doxyfile if returned by LLM
        if "updated_doxyfile" in parsed:
            os.makedirs(os.path.dirname(doxyfile_path), exist_ok=True)
            with open(doxyfile_path, "w", encoding="utf-8") as f:
                f.write(parsed["updated_doxyfile"])

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

class DeploymentStrategyResolver(Agent):
    """
    Resolves and validates deployment strategy from user preferences.
    Deterministic, strict validation.
    """

    def __init__(self):
        super().__init__("DeploymentStrategyResolver", depends_on=[])

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):
        logger.info(f"[{self.name}] start running")
        prefs = task.get("deployment_preferences", {})

        if not prefs:
            raise ValueError("deployment_preferences is required")

        strategy = {
            "type": prefs.get("type"),
            "platform": prefs.get("platform"),
            "branch": prefs.get("branch", "main"),
            "docs_path": prefs.get("docs_path", "docs"),
            "custom_domain": prefs.get("custom_domain"),
            "docker_image": prefs.get("docker_image"),      # container
            "k8s_namespace": prefs.get("k8s_namespace"),    # kubernetes
            "server_user": prefs.get("server_user"),        # server
            "cloud_bucket": prefs.get("cloud_bucket")       # cloud
        }

        valid_types = ["static", "container", "kubernetes", "server", "cloud"]

        valid_platforms = {
            "static": ["github_pages", "gitlab_pages", "netlify", "vercel", "s3"],
            "container": ["docker"],
            "kubernetes": ["k8s"],
            "server": ["nginx", "apache"],
            "cloud": ["s3", "cloudfront"]
        }

        # ----------------------------
        # VALIDATION
        # ----------------------------
        if strategy["type"] not in valid_types:
            raise ValueError(f"Invalid deployment type: {strategy['type']}")

        if strategy["platform"] not in valid_platforms.get(strategy["type"], []):
            raise ValueError(
                f"Incompatible platform '{strategy['platform']}' for type '{strategy['type']}'"
            )

        crew_context[self.name] = strategy
        return strategy

class DocumentationDeploymentGenerator(Agent):
    """
    Production-grade deployment generator for documentation systems.
    LLM-driven but strictly constrained.
    """

    def __init__(self):
        super().__init__(
            "DocumentationDeploymentGenerator",
            depends_on=[
                "DeploymentStrategyResolver",
                "DoxygenConfigBuilder",
                "DoxygenDocumentationUXBuilder",
                "DevOpsAnalyzer",
                "ProjectMetadataAnalyzer"
            ]
        )

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):

        logger.info(f"[{self.name}] start running")

        project_root = task.get("project_root", ".")
        strategy = crew_context.get("DeploymentStrategyResolver")

        if not strategy:
            raise RuntimeError("Deployment strategy not resolved")

        context = {k: crew_context.get(k, {}) for k in self.depends_on}

        prompt = f"""
            You are a senior DevOps engineer specialized in documentation systems.

            ==================================================
            DEPLOYMENT STRATEGY (STRICT INPUT):
            {json.dumps(strategy, indent=2)}

            FULL PROJECT CONTEXT:
            {json.dumps(context, indent=2)}

            ==================================================
            MANDATORY RULES:

            - DO NOT infer anything
            - DO NOT change strategy
            - DO NOT ask questions
            - FOLLOW strategy strictly

            ==================================================
            GLOBAL REQUIREMENTS:

            1. Build system:
            - Provide build_docs.sh (bash)
            - Must be idempotent
            - Must fail on error (set -e)

            2. Doxygen:
            - Execute using provided config
            - Respect OUTPUT_DIRECTORY from config
            - Integrate Markdown
            - Include diagrams if available

            3. Post-processing:
            - Copy UI assets
            - Fix relative paths
            - Ensure deploy-ready structure

            4. Output:
            - Use correct output directory from Doxygen
            - Ensure static hosting compatibility

            ==================================================
            CI/CD REQUIREMENTS (MANDATORY):

            - Install dependencies (doxygen, graphviz, etc.)
            - Use caching if possible
            - Upload artifacts
            - Restrict to main/master branch
            - Use production-ready actions/templates

            ==================================================
            TYPE-SPECIFIC REQUIREMENTS:

            ### STATIC:

            Platform-specific behavior:
            - github_pages → .github/workflows/docs.yml
            - gitlab_pages → .gitlab-ci.yml
            - netlify/vercel → config files

            Must:
            - deploy generated HTML
            - handle base path issues

            ### CONTAINER:

            Must generate:
            - Dockerfile (multi-stage)
            - docker-compose.yml

            Dockerfile MUST:
            - use nginx:alpine
            - copy only built docs
            - expose port 80

            ### KUBERNETES:

            Must generate:
            - deployment.yaml
            - service.yaml
            - ingress.yaml

            Use:
            - nginx container
            - proper labels/selectors

            ### SERVER:

            Must generate:
            - deploy.sh (scp + ssh)
            - nginx.conf

            ### CLOUD (S3):

            Must generate:
            - deploy script using aws cli
            - sync command
            - optional cloudfront invalidation

            ==================================================
            OUTPUT FORMAT (STRICT JSON):

            {{
            "files": [
                {{
                "path": "",
                "content": ""
                }}
            ]
            }}

            Return ONLY JSON.
            """

        result = llm_run(prompt, max_tokens=6000)
        parsed = extract_json(result)

        # ----------------------------
        # VALIDATION
        # ----------------------------
        if not parsed or "files" not in parsed:
            raise RuntimeError("Invalid deployment generation output")

        # ----------------------------
        # WRITE FILES
        # ----------------------------
        for f in parsed["files"]:
            path = os.path.join(project_root, f["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)

            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(f["content"])
            except Exception as e:
                logger.error(f"Error writing {path}: {e}")

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed


# ----------------------------
# Crew
# ----------------------------

class Crew:

    def __init__(self, max_workers=8):
        self.agents = []
        self.max_workers = max_workers
        self.context_lock = threading.Lock()

    def add_agent(self, agent: Agent):
        # Passiamo il lock all'agente al momento dell'aggiunta
        agent.lock = self.context_lock
        self.agents.append(agent)

    def verify_dag(self):
        """Verifica che non ci siano cicli nelle dipendenze prima di partire."""
        dag = nx.DiGraph()
        for agent in self.agents:
            dag.add_node(agent.name)
            for dep in agent.depends_on:
                dag.add_edge(dep, agent.name)
        
        if not nx.is_directed_acyclic_graph(dag):
            cycle = nx.find_cycle(dag, orientation="original")
            raise Exception(f"Deadlock rilevato: dipendenze circolari {cycle}")
        logger.info("[Crew] DAG validato con successo.")

    def run(self, task: dict) -> dict:
        logger.info(f"[Crew] verify DAG..")
        self.verify_dag()
        
        logger.info(f"[Crew] start running")
        
        crew_context = {"results": {}}
        completed_agents = set()
        failed_agents = set()
        active_futures = {}
        
        # Lock per proteggere le strutture dati del loop
        scheduling_lock = threading.Lock()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while len(completed_agents) + len(failed_agents) < len(self.agents):
                
                with scheduling_lock:
                    for agent in self.agents:
                        if agent.name in completed_agents or agent.name in failed_agents or agent.name in active_futures:
                            continue
                        
                        if all(dep in completed_agents for dep in agent.depends_on):
                            if any(dep in failed_agents for dep in agent.depends_on):
                                failed_agents.add(agent.name)
                                continue
                                
                            future = executor.submit(self.run_agent, agent, task, crew_context)
                            active_futures[agent.name] = future

                # Gestione completamento
                if active_futures:
                    done, _ = wait(list(active_futures.values()), return_when=FIRST_COMPLETED)
                    with scheduling_lock:
                        for agent_name, future in list(active_futures.items()):
                            if future in done:
                                try:
                                    future.result() # Qui il wrapper ha già salvato il risultato
                                    completed_agents.add(agent_name)
                                except Exception as e:
                                    logger.critical(f"[Crew] Critical Error in {agent_name}: {e}")
                                    failed_agents.add(agent_name)
                                del active_futures[agent_name]
                time.sleep(0.1)
        
        return crew_context["results"]

    def run_agent(self, agent, task, crew_context):
        """Esegue l'agente e salva centralmente il risultato."""
        output = agent.run(task, crew_context)
        with self.context_lock:
            crew_context["results"][agent.name] = output
        logger.info(f"[Crew] Risultato di {agent.name} salvato.")

        

def load_project_context(path="./project_context.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    logger.info("\n=== AVVIO DOXYGEN AI CREW ===\n")

    # ----------------------------
    # Lettura nuovo progetto
    # ----------------------------
    src_files = read_project_files(SRC_PATH)

    project_context = load_project_context()

    logger.info("project context: " + str(project_context))
    task = {
        "project_context": project_context,
        "repos": [
                {"owner": "pallets", "repo": "flask"},
                {"owner": "fastapi", "repo": "fastapi"}
        ],
        "github_token": GITHUB_TOKEN,
        "github_username": GITHUB_USERNAME,
        "cohere_api_key": COHERE_API_KEY,  # se necessario
        "project_root": "./docs",          # cartella dove generare doc
        "files_dict": src_files,           # dizionario file sorgente
        "deployment_preferences": {
            "type": "static",
            "platform": "github_pages",
            "branch": "main",
            "docs_path": "docs",
            "custom_domain": None
        }
    }

    # ----------------------------
    # Inizializzazione Crew
    # ----------------------------
    crew = Crew()

    crew.add_agent(ProjectTreeAnalyzer())
    crew.add_agent(LanguageDetector())
    crew.add_agent(DependencyDetector())
    crew.add_agent(BuildSystemDetector())
    crew.add_agent(CodeArchitectureAnalyzer())
    crew.add_agent(APIAnalyzer())
    crew.add_agent(SecurityPermissionAnalyzer())
    crew.add_agent(UsageAnalyzer())
    crew.add_agent(DocumentationAnalyzer())
    crew.add_agent(DevOpsAnalyzer())
    crew.add_agent(VersioningAnalyzer())
    crew.add_agent(QualityAnalyzer())
    crew.add_agent(ProjectMetadataAnalyzer())
    crew.add_agent(MDTemplateAnalyzer())
    crew.add_agent(MDDocumentationMaker())
    #crew.add_agent(DoxygenConfigBuilder())
    #crew.add_agent(DoxygenDocumentationUXBuilder())
    #crew.add_agent(DeploymentStrategyResolver())
    #crew.add_agent(DocumentationDeploymentGenerator())

    # ----------------------------
    # Esecuzione
    # ----------------------------
    results = crew.run(task)

    logger.info("\n=== RISULTATI CREW ===\n")

    for agent_name, output in results.items():
        logger.info(f"\n--- {agent_name} ---")

        if isinstance(output, dict):
            logger.info(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            logger.info(output)


    logger.info("\n=== FINE ESECUZIONE ===\n")