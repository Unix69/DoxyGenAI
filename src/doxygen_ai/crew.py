import os
import sys
import logging

# Aggiunge src/doxygen_ai al path, così Python trova agents
sys.path.append(os.path.dirname(__file__))

# Configura logging base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Debug info sul container
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python sys.path: {sys.path}")

# Import moduli con gestione errori
try:
    from crewai import Crew, CrewBase
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
except Exception as e:
    logger.exception("Errore durante l'import dei moduli")
    with open("/tmp/deploy_error.log", "w") as f:
        f.write(str(e))
    raise

# Definizione degli agenti
try:
    AGENTS = [LanguageDetector()]
    logger.info("LanguageDetector istanziato correttamente")
except Exception as e:
    logger.exception("Errore durante l'istanza di LanguageDetector")
    with open("/tmp/deploy_error.log", "w") as f:
        f.write(str(e))
    raise

# Definizione della classe Crew annotata per Enterprise
@CrewBase
class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=AGENTS,
            process="sequential",
            verbose=True
        )
        logger.info("DoxygenCrew creato correttamente")