import os
import sys
import logging
import pkg_resources

# Aggiunge src/doxygen_ai al path per trovare agents
sys.path.append(os.path.dirname(__file__))

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Mostra informazioni sul container
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python sys.path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")

# Debug: mostra versioni dei pacchetti installati
for pkg in ["crewai", "crewai-enterprise"]:
    try:
        version = pkg_resources.get_distribution(pkg).version
        logger.info(f"{pkg} version: {version}")
        print(f"{pkg} version: {version}")
    except pkg_resources.DistributionNotFound:
        logger.warning(f"{pkg} non installato")
        print(f"{pkg} non installato")

# Controllo variabili d'ambiente richieste
required_env = ["OPENAI_API_KEY"]
for var in required_env:
    if not os.getenv(var):
        msg = f"Variabile d'ambiente {var} non impostata!"
        print(msg)
        logger.error(msg)
        raise EnvironmentError(msg)

# Import moduli con gestione errori
try:
    from crewai import Crew
    from agents.LanguageDetector import LanguageDetector
    logger.info("LanguageDetector importato correttamente")
    print("LanguageDetector importato correttamente")
except Exception as e:
    logger.exception("Errore durante l'import dei moduli")
    print(f"Errore durante l'import dei moduli: {e}")
    raise

# Definizione agenti
try:
    AGENTS = [LanguageDetector()]
    logger.info("LanguageDetector istanziato correttamente")
    print("LanguageDetector istanziato correttamente")
except Exception as e:
    logger.exception("Errore durante l'istanza di LanguageDetector")
    print(f"Errore durante l'istanza di LanguageDetector: {e}")
    raise

# Classe Crew compatibile con tutte le versioni
class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=AGENTS,
            process="sequential",
            verbose=True
        )
        logger.info("DoxygenCrew creato correttamente")
        print("DoxygenCrew creato correttamente")