import os
import sys
import logging
from crewai import Crew, Task

# Aggiunge src/doxygen_ai al path
sys.path.append(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.info(f"Current working directory: {os.getcwd()}")

# Controllo chiave API
if not os.getenv("OPENAI_API_KEY"):
    msg = "Variabile d'ambiente OPENAI_API_KEY non impostata!"
    logger.error(msg)
    raise EnvironmentError(msg)
logger.info("OPENAI_API_KEY trovata correttamente")


# Task interno per aggiungere LanguageDetector dinamicamente
class _AutoAddLanguageDetector(Task):
    async def run(self, task_input):
        logger.info("Esecuzione task _AutoAddLanguageDetector...")
        crew = task_input.crew  # Crew già in Running automation

        try:
            from agents.LanguageDetector import LanguageDetector
            ld = LanguageDetector()
            crew.add_agent(ld)
            logger.info("LanguageDetector aggiunto automaticamente alla Crew")
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Errore aggiungendo LanguageDetector: {e}")
            return {"status": "failed", "message": str(e)}


# Crew principale
class DoxygenCrew(Crew):
    def __init__(self):
        # Partenza senza agenti → deploy stabile
        super().__init__(agents=[], process="sequential", verbose=True)
        logger.info("DoxygenCrew avviata senza agenti")

        # Esegue il task automatico di bootstrap senza bloccare il deploy
        # Nota: self.schedule_task lo esegue dopo che la Crew è online
        self.schedule_task(_AutoAddLanguageDetector())
        logger.info("Task automatico per LanguageDetector schedulato")