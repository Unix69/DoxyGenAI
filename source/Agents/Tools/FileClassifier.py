import os
import threading


from dotenv import load_dotenv

from Agents.Tools.Tools import extract_json, take_first_lines, to_b64
from Agents.Tools.LLM import llm_run

 
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
USE_COHERE = os.getenv("USE_COHERE", "false").lower() == "true"
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
USE_DEEPSEEK = os.getenv("USE_DEEPSEEK", "false").lower() == "true"
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
USE_GROK = os.getenv("USE_GROK", "false").lower() == "true"
SRC_PATH=os.getenv("SRC_PATH")
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "doxygen_ai_crew.log")
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-xlarge-nightly")  
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_URL = os.getenv("COHERE_URL", "")
OPENAI_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROK_URL = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-beta")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL", "gemini-1.5-flash")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

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

