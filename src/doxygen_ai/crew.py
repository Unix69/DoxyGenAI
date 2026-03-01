import os
import sys
import logging

# Aggiunge la cartella src/doxygen_ai al path
sys.path.append(os.path.dirname(__file__))

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python sys.path: {sys.path}")

# Controllo chiave API
if not os.getenv("OPENAI_API_KEY"):
    msg = "Variabile d'ambiente OPENAI_API_KEY non impostata!"
    logger.error(msg)
    raise EnvironmentError(msg)
logger.info("OPENAI_API_KEY trovata correttamente")

# Import moduli
try:
    from crewai import Crew
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
except Exception as e:
    logger.exception(f"Errore durante l'import dei moduli: {e}")
    raise

# Istanzia LanguageDetector con gestione errori
try:
    ld = LanguageDetector()
    logger.info("LanguageDetector istanziato correttamente")
except Exception as e:
    ld = None
    logger.warning(f"LanguageDetector NON istanziato: {e}")

# Definizione Crew
class DoxygenCrew(Crew):
    def __init__(self):
        AGENTS = []
        if ld:
            AGENTS.append(ld)
            logger.info("LanguageDetector aggiunto agli agenti")
        else:
            logger.warning("Crew parte senza LanguageDetector")
        super().__init__(agents=AGENTS, process="sequential", verbose=True)
        logger.info("DoxygenCrew creata correttamente")