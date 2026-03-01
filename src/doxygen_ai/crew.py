import os
import sys
import logging

# Aggiunge src/doxygen_ai al path
sys.path.append(os.path.dirname(__file__))

# Configura il logging base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

try:
    from crewai import Crew
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
except Exception as e:
    logger.exception("Errore durante l'import dei moduli")
    raise

# Definizione agenti
AGENTS = [LanguageDetector()]

# Creazione del Crew
crew = Crew(
    agents=AGENTS,
    process="sequential",
    verbose=True
)