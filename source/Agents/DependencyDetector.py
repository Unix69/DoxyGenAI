import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class DependencyDetector(Agent):

    def __init__(self):
        super().__init__("DependencyDetector")

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        
        # 1. Recupera i dati di input dal task
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)

        # filtra solo file utili per analisi dipendenze
        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["build", "config", "source"]
        }

        snippets = take_first_lines(relevant_files, 2000)
        files_b64 = to_b64(snippets)

        prompt = f"""
            You are a software dependency analysis engine.

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILES_B64:
            {files_b64}

            Detect:

            - runtime_dependencies
            - build_dependencies
            - development_dependencies
            - external_services
            - system_dependencies
            - package_managers
            - dependency_versions

            Return JSON:

            {{
            "runtime_dependencies": [],
            "build_dependencies": [],
            "development_dependencies": [],
            "external_services": [],
            "system_dependencies": [],
            "package_managers": [],
            "dependency_versions": {{}},
            "dependency_management_strategy": ""
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.


            """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error":"invalid_json","raw":result}
        self.save_to_json(data=parsed, raw_content=result)
        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed