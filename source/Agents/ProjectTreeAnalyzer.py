import json
from typing import Any, Dict


from Agents.Tools.Tools import extract_json

from Agents.Tools.LLM import llm_run

from Agents.Logger import logger
from Agents.Agent import Agent

class ProjectTreeAnalyzer(Agent):

    def __init__(self):
        super().__init__("ProjectTreeAnalyzer")

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):

        logger.info(f"[{self.name}] start running")

        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result

        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        
        # Estrae l'elenco dei percorsi dei file per creare l'albero
        file_paths = list(files_dict.keys())
        print("This are the file_paths compeleted: " + str(file_paths))

        prompt = f"""
            You are a senior software architect.

            Analyze the FILE PATHS of a software project.

            Infer the project structure and directory organization.

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILE_PATHS:
            {json.dumps(file_paths, indent=2)}

            Infer:

            - directory_tree (each directory and each file recursivly contained into)
            - root_modules
            - src_directory_present
            - tests_directory_present
            - docs_directory_present
            - config_directory_present
            - scripts_directory_present
            - packaging_files
            - average_directory_depth
            - project_layout_type
            (monolithic | modular | layered | microservices | library | embedded)

            Return STRICT JSON:

            {{
            "directory_tree": {{}},
            "root_modules": [],
            "src_directory_present": true,
            "tests_directory_present": true,
            "docs_directory_present": true,
            "config_directory_present": true,
            "scripts_directory_present": true,
            "packaging_files": [],
            "average_directory_depth": 0,
            "project_layout_type": "",
            "directory_conventions": []
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            If something cannot be deduced return null.
            """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)
        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed