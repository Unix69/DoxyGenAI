from crewai import Agent, Task

class TestAgent(Agent):
    role: str = "Test"
    goal: str = "Test deploy"
    backstory: str = "Minimal agent"
    allow_llm: bool = False

    async def run(self, task: Task):
        return {"status": "ok"}