from crewai import Agent, Task
import logging

logger = logging.getLogger("main")



class DummyAgent(Agent):
    role: str = "Dummy agent role"
    goal: str = "Testing if run() is called"
    backstory: str = "Used for testing Crew execution"
    allow_llm: bool = True  # permette l'esecuzione senza LLM

    async def run(self, task: Task):
        logger.info(">>> DummyAgent.run chiamato!")
        logger.info(f"Task ricevuto: {task}")
        return {"ok": True}