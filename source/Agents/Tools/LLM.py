import os
import cohere
from openai import OpenAI
from dotenv import load_dotenv
import time
import threading
from Agents.Tools.Tools import extract_json
import google.generativeai as genai
import tiktoken
from Agents.Logger import logger


load_dotenv()



USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
USE_COHERE = os.getenv("USE_COHERE", "false").lower() == "true"
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
USE_DEEPSEEK = os.getenv("USE_DEEPSEEK", "false").lower() == "true"
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
USE_GROK = os.getenv("USE_GROK", "false").lower() == "true"
SRC_PATH=os.getenv("SRC_PATH")
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


class LLMProvider:
    def __init__(self, name):
        self.name = name

    def chat(self, prompt, max_tokens, temperature):
        raise NotImplementedError
    

class OllamaProvider(LLMProvider):
    def __init__(self, model_name="llama3"):
        super().__init__("ollama")
        # Ollama espone le API in formato OpenAI sulla porta 11434
        self.client = OpenAI(
            base_url=OLLAMA_URL,
            api_key="ollama" # La chiave non è necessaria in locale
        )
        self.model_name = model_name

    def chat(self, prompt, max_tokens, temperature):
        res = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return res.choices[0].message.content
    


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, base_url, model_name):
        super().__init__("openai")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def chat(self, prompt, max_tokens, temperature):
        res = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return res.choices[0].message.content

class CohereProvider(LLMProvider):
    def __init__(self, api_key, model_name):
        super().__init__("cohere")
        self.client = cohere.Client(api_key)
        self.model_name = model_name

    def chat(self, prompt, max_tokens, temperature):
        return self.client.chat(
            model=self.model_name,
            message=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        ).text

class DeepSeekProvider(LLMProvider):
    def __init__(self, api_key, base_url, model_name):
        super().__init__("deepseek")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def chat(self, prompt, max_tokens, temperature):
        res = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return res.choices[0].message.content

class GeminiProvider(LLMProvider):
    def __init__(self, api_key, model_name):
        super().__init__("gemini")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, prompt, max_tokens, temperature):
        response = self.model.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_tokens, "temperature": temperature}
        )
        return response.text

class FallbackProvider(LLMProvider):
    def __init__(self):
        super().__init__("fallback")

    def chat(self, prompt, max_tokens, temperature):
        return "FALLBACK RESPONSE (no provider available)"




# 2. Inizializza i provider dinamicamente
providers = []

if USE_GEMINI and GEMINI_API_KEY and GEMINI_MODEL:
    providers.append(GeminiProvider(GEMINI_API_KEY, GEMINI_MODEL))

if USE_COHERE and COHERE_API_KEY:
    providers.append(CohereProvider(COHERE_API_KEY, COHERE_MODEL))

if USE_DEEPSEEK and DEEPSEEK_API_KEY and DEEPSEEK_MODEL:
    providers.append(DeepSeekProvider(DEEPSEEK_API_KEY, DEEPSEEK_URL, DEEPSEEK_MODEL))

if USE_OPENAI and OPENAI_API_KEY and OPENAI_MODEL:
    providers.append(OpenAIProvider(OPENAI_API_KEY, OPENAI_URL, OPENAI_MODEL))

if USE_GROK and GROK_API_KEY and GROK_MODEL:
    providers.append(OpenAIProvider(GROK_API_KEY, GROK_URL, GROK_MODEL))

if USE_OLLAMA and OLLAMA_MODEL:
    providers.append(OllamaProvider(model_name=OLLAMA_MODEL))


providers.append(FallbackProvider())

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
                logger.info(f"[GlobalRateLimiter] wait {sleep_time:.2f}s")
                time.sleep(sleep_time)
            
            self.last_call = time.time()

    def report_llm_boundary_error(self):
        """Chiamato quando riceviamo un errore 429"""
        with self.lock:
            # Aumentiamo drasticamente il delay in caso di blocco
            self.min_delay = min(self.min_delay * 1.5, self.max_delay)
            logger.warning(f"[GlobalRateLimiter] llm boundary error. delay increased to {self.min_delay:.2f}s")

    def report_success(self):
        """Chiamato quando la chiamata ha successo"""
        with self.lock:
            # Recupero lento: se tutto va bene, torniamo verso il basso
            if self.min_delay > 3.0:
                self.min_delay = max(self.min_delay * 0.9, 3.0)
            logger.info(f"[GlobalRateLimiter] llm boundary error. delay decreased to {self.min_delay:.2f}s")


rate_limiter = GlobalRateLimiter(base_delay=1.2)



class TokenBudgetManager:

    def __init__(self, model_limit=288000, output_reserve=4000):
        self.model_limit = model_limit
        self.output_reserve = output_reserve

    def count_tokens(self, text: str) -> int:
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
        logger.info(f"[LLM] Chunk mode activated | tokens={prompt_tokens}")

        chunks = chunk_prompt(prompt, 12000)
        context_memory = ""
        total_attempts = 0

        
        for provider in providers:
            logger.info(f"[LLM-CHUNK] Running llm [{provider.name}]")
            for i, chunk in enumerate(chunks):

                chunk_success = False

                partial_prompt = None
                text = None

                for attempt in range(retries):
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

                        if "429" in str(e) or "402" in str(e):
                            logger.warning(f"[LLM-CHUNK] Error on {provider.name} | error='{str(e)}'")
                            rate_limiter.report_llm_boundary_error()
                            continue

                        logger.warning(f"[LLM-CHUNK] Error on {provider.name} | error='{str(e)}'")
                        continue

                if chunk_success:
                    break

            if not chunk_success:
                logger.error(f"[LLM-CHUNK] Max llm-chunk send retries reached in CHUNK MODE| error='Chunk {i} failed'")
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

        logger.info(f"[LLM-CHUNK] Chunks merge running | memory_prompt={merge_prompt} | max_tokens={max_tokens} | safe_max_tokens={safe_max}")
        
        last_error = None

        for attempt in range(1, retries + 1):  # global retry

            rate_limiter.wait()

            for provider in providers:  # failover providers
                logger.info(f"[LLM-CHUNK] Running llm | provider='{provider.name}'")
                try:
                    response_text = provider.chat(
                        prompt=merge_prompt,
                        max_tokens=safe_max,
                        temperature=temperature
                    )

                    text = (response_text or "").strip()

                    if not text:
                        raise ValueError("Empty merge response")

                    
                    logger.info(f"[LLM-CHUNK] llm [{provider.name}] response {str(text)}")
                    rate_limiter.report_success()


                    parsed = extract_json(text) if expect_json else text

                    logger.info(f"[LLM-CHUNK] llm [{provider.name}] json parsed response {str(parsed)}")
                    logger.info(f"[LLM-CHUNK] llm [{provider.name}] run success")

                    return LLMResult(
                        ok=True,
                        data=parsed,
                        raw=text,
                        attempts=attempt
                    )

                except Exception as e:
                    last_error = str(e)

                    if "429" in str(e) or "402" in str(e):
                        logger.warning(f"[LLM-CHUNK] Error on llm | provider='{provider.name}' | error='{str(e)}'")
                        rate_limiter.report_llm_boundary_error()
                        continue

                    logger.warning(f"[LLM-CHUNK] Error on llm | provider='{provider.name}' | error='{str(e)}'")
                    continue

            # se tutti i provider falliscono → backoff globale
            sleep_time = backoff_base ** (attempt - 1)
            logger.warning(f"[LLM-CHUNK] all providers failed | retrying in sleeptime='{sleep_time:.2f}s'")
            time.sleep(sleep_time)

        logger.error("[LLM-CHUNK] Max merge send retries reached in CHUNK MODE.")
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
                logger.info(f"[LLM] Running llm | provider='{provider.name}' | max_tokens={max_tokens} | safe_max_tokens={safe_max}")
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

                logger.info(f"[LLM] llm | provider='{provider.name}' | json parsed response={str(parsed)}")
                logger.info(f"[LLM] llm | provider='{provider.name}' run success")

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
                last_error = str(e)
                if "429" in str(e) or "402" in str(e):
                    logger.warning(f"[LLM] Error on llm | provider='{provider.name}' | error='{str(e)}'")
                    rate_limiter.report_llm_boundary_error()
                    continue

                logger.warning(f"[LLM] Error on llm | provider='{provider.name}' | error='{str(e)}'")
                continue

        # =========================================================
        # ALL PROVIDERS FAILED IN THIS ATTEMPT → BACKOFF
        # =========================================================
        sleep_time = backoff_base ** (attempt - 1)
        logger.warning(f"[LLM] All providers failed | retrying in sleeptime='{sleep_time:.2f}s'")
        time.sleep(sleep_time)

    # =========================================================
    # FINAL FAILURE
    # =========================================================
    logger.error("[LLM] Max llm send retries reached in NORMAL MODE.")
    return LLMResult(
        ok=False,
        error=str(last_error),
        attempts=retries
    )

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