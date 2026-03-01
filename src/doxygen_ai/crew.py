from crewai import Crew, Task
from doxygen_ai.agents.TestAgent import TestAgent

class DoxygenAiCrew(Crew):
    def __init__(self):
        agent = TestAgent()

        task = Task(
            description="Test execution",
            agent=agent
        )

        super().__init__(
            agents=[agent],
            tasks=[task],
            process="sequential",
            verbose=True
        )