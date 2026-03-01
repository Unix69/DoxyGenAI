from crewai import Crew
from doxygen_ai.agents.TestAgent import TestAgent

class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=[TestAgent()],
            process="sequential",
            verbose=True
        )