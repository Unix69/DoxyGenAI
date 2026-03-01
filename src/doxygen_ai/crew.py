import logging
from crewai import Crew, Agent
from agents.LanguageDetector import LanguageDetector


logger = logging.getLogger("main")

AGENTS = [
    LanguageDetector()
]

crew = Crew(
    agents=AGENTS,
    process="sequential",
    verbose=True
)