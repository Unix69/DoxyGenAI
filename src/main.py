import os
import asyncio
import logging
from crewai import Flow
from crew import crew
from tasks import language_detection_task

# Logger globale
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

os.environ["CREWAI_DISABLE_LLM"] = "false"
os.environ["CREWAI_TRACING_ENABLED"] = "true"

def scan_files(path):
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files

# --- Step del Flow ---
async def bootstrap(context):
    logger.info(">>> bootstrap step iniziato")
    context.state["src"] = "./src"
    context.state["template"] = scan_files("./template")
    return "run_agent"

async def run_agent(context):
    task = language_detection_task(crew.agents[0], context.state["src"], context.state["template"])
    result = await crew.agents[0].run(task)
    context.state["result"] = result
    return "finish"

async def finish(context):
    print("Result:", context.state["result"])
    return None

flow = Flow(name="LanguageDetector", start="bootstrap")
flow.steps = {
    "bootstrap": bootstrap,
    "run_agent": run_agent,
    "finish": finish
}

if __name__ == "__main__":
    crew.verbose = True

    mode = os.environ.get("FLOW_MODE", "async")  # default async

    if mode == "async":
        logger.info("=== Avvio flow in modalità ASINCRONA ===")
        asyncio.run(flow.kickoff_async())
    else:
        logger.info("=== Avvio flow in modalità SINCRONA ===")
        flow.kickoff()  # metodo sincrono