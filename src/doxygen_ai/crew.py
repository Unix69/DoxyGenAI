import os
import sys
import logging

# Aggiunge src/doxygen_ai al path, così Python trova il pacchetto agents
sys.path.append(os.path.dirname(__file__))

# Configura logging base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Stampa informazioni di debug su path e directory
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python sys.path: {sys.path}")

# Import dei moduli con gestione errori
try:
    from crewai import Crew
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
except Exception as e:
    logger.exception("Errore durante l'import dei moduli")
    # Scrive anche su file temporaneo nel container per debug
    with open("/tmp/deploy_error.log", "w") as f:
        f.write(str(e))
    raise

# Creazione degli agenti
AGENTS = []
try:
    ld = LanguageDetector()
    AGENTS.append(ld)
    logger.info("LanguageDetector istanziato correttamente")
except Exception as e:
    logger.exception("Errore durante l'istanza di LanguageDetector")
    with open("/tmp/deploy_error.log", "w") as f:
        f.write(str(e))
    raise

# Creazione del Crew
try:
    crew = Crew(
        agents=AGENTS,
        process="sequential",
        verbose=True
    )
    logger.info("Crew creato correttamente")
except Exception as e:
    logger.exception("Errore durante la creazione del Crew")
    with open("/tmp/deploy_error.log", "w") as f:
        f.write(str(e))
    raise