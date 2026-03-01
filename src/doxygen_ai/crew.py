from crewai import Crew
from doxygen_ai.agents.TestAgent import TestAgent

class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(agents=[], process="sequential", verbose=True)
        # Aggiungi l'agente minimale
        self.add_agent(TestAgent())