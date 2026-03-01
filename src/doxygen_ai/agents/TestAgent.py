# agents/TestAgent.py
from crewai import Agent, Task

class TestAgent(Agent):
    role: str = "Agente di test minimale"
    goal: str = "Serve solo a verificare che la Crew deployi senza errori"
    backstory: str = "Agente fittizio per test"
    allow_llm: bool = False  # Non usare LLM per evitare problemi al deploy

    async def run(self, task: Task):
        print(">>> TestAgent.run chiamato!")
        # Restituisce un risultato semplice
        return {"status": "ok"}