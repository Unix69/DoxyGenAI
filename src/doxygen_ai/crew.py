import os
import sys
import logging

# Aggiunge src/doxygen_ai al path per trovare agents
sys.path.append(os.path.dirname(__file__))

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Debug info sul container
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python sys.path: {sys.path}")

# Controllo variabili d'ambiente richieste
required_env = ["OPENAI_API_KEY"]
for var in required_env:
    if not os.getenv(var):
        msg = f"Variabile d'ambiente {var} non impostata!"
        print(msg)   # comparirà subito nei log runtime
        logger.error(msg)
        raise EnvironmentError(msg)

# Import moduli con gestione errori
try:
    from crewai import Crew
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
    print("LanguageDetector importato correttamente")
except Exception as e:
    print(f"Errore durante l'import dei moduli: {e}")
    logger.exception("Errore durante l'import dei moduli")
    raise

# Definizione agenti
try:
    AGENTS = [LanguageDetector()]
    logger.info("LanguageDetector istanziato correttamente")
    print("LanguageDetector istanziato correttamente")
except Exception as e:
    print(f"Errore durante l'istanza di LanguageDetector: {e}")
    logger.exception("Errore durante l'istanza di LanguageDetector")
    raise

# Classe Crew moderna (senza @CrewBase)
class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=AGENTS,
            process="sequential",
            verbose=True
        )
        logger.info("DoxygenCrew creato correttamente")
        print("DoxygenCrew creato correttamente")