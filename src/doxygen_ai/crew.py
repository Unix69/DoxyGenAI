from crewai import Crew
from agents.LanguageDetector import LanguageDetector

class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(agents=[], process="sequential", verbose=True)
        
        # aggiunge LanguageDetector in modo sicuro
        ld = LanguageDetector()
        self.add_agent(ld)