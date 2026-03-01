from crewai import Agent, Task

class TestAgent(Agent):
    role = "Test"
    goal = "Test deploy"
    backstory = "Minimal agent"
    allow_llm = False

    async def run(self, task: Task):
        return {"status": "ok"}