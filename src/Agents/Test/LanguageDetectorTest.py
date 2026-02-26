import asyncio
from Agents.LanguageDetector import LanguageDetector
from tasks import language_detection_task
import logging

logger = logging.getLogger("main")


agent = LanguageDetector()

# Creo un task direttamente
task = language_detection_task(agent, "./src", "./template")

async def test_run():
    result = await agent.run(task)   # richiamata diretta
    print("Result:", result)

asyncio.run(test_run())