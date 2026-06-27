import json
from typing import Any, Dict
from Agents.Agent import Agent
from Agents.Logger import logger
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run

class UsageAnalyzer(Agent):
    """
    Analizza i casi d'uso principali del progetto.
    Integra informazioni API, architettura, directory e dipendenze.
    """

    def __init__(self):
        super().__init__("UsageAnalyzer", depends_on=["APIAnalyzer", "CodeArchitectureAnalyzer", "ProjectTreeAnalyzer", "DependencyDetector", "BuildSystemDetector"])

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Seleziona solo file rilevanti: source e config ad alta confidenza
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=None)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config"] and f.get("confidence", 0) > 0.6
        }

        # 2. Integra informazioni dai principali agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        architecture_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        dependency_info = self.get_agent_output(crew_context, "DependencyDetector")
        build_info = self.get_agent_output(crew_context, "BuildSystemDetector")

        # 3. Prepara i dati da passare al LLM
        input_payload = {
            "files_b64": to_b64(relevant_files),
            "api_info": api_info,
            "architecture_info": architecture_info,
            "project_tree": project_tree,
            "dependency_info": dependency_info,
            "build_info": build_info
        }

        # 4. Prompt ottimizzato
        prompt = f"""
        You are a senior software architect and system analyst.

        Given the following project information:

        PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

        FILES (source and config, base64):
        {input_payload['files_b64']}

        API INFO:
        {json.dumps(input_payload['api_info'], indent=2)}

        ARCHITECTURE INFO:
        {json.dumps(input_payload['architecture_info'], indent=2)}

        PROJECT TREE:
        {json.dumps(input_payload['project_tree'], indent=2)}

        DEPENDENCIES:
        {json.dumps(input_payload['dependency_info'], indent=2)}

        BUILD INFO:
        {json.dumps(input_payload['build_info'], indent=2)}

        Infer the main use cases, including:

        - use case names
        - actors
        - roles
        - workflows
        - features
        - APIs used per use case
        - namespaces involved

        Return STRICT JSON:

        {{
            "use_cases":[
                {{
                    "name":"",
                    "actors":[],
                    "roles":[],
                    "features":[],
                    "apis":[],
                    "namespaces":[]
                }}
            ]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=8000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed
