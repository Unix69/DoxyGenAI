import os
from crewai import Agent, Task
import logging

logger = logging.getLogger("main")


class LanguageDetector(Agent):
    role: str = "Rilevamento linguaggi e build script"
    goal: str = (
        "Analizza i file sorgente nella cartella src e gli script/config "
        "del template per rilevare linguaggi principali, linguaggi impliciti "
        "e la presenza di build/test/deploy script."
    )
    backstory: str = "Agente specializzato nell'analisi strutturale di progetti software."
    allow_llm: bool = False

    async def run(self, task: Task):
        logger.info(">>> LanguageDetector.run chiamato!")
        src = task.input_files.get("src", "./src")
        template = task.input_files.get("template", [])
        logger.info(f"Input ricevuto dal task: {{'src': '{src}', 'template': {template}}}")

        extensions = {}
        has_build_scripts = False

        for root, _, files in os.walk(src):
            for f in files:
                ext = os.path.splitext(f)[1]
                extensions[ext] = extensions.get(ext, 0) + 1
                if f in ["Makefile", "doxygen.sh", "doxygen.ini", "Doxyfile"]:
                    has_build_scripts = True

        primary_language = max(extensions, key=extensions.get) if extensions else None
        multi_language = len(extensions) > 1

        for f in template:
            ext = os.path.splitext(f)[1]
            if ext not in extensions:
                extensions[ext] = 0

        result = {
            "languages": list(extensions.keys()),
            "primary_language": primary_language,
            "multi_language": multi_language,
            "has_build_scripts": has_build_scripts
        }

        logger.info(f"Output generato: {result}")
        return result