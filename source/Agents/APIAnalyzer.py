import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class APIAnalyzer(Agent):

    def __init__(self):
        super().__init__(
            "APIAnalyzer",
            depends_on=["CodeArchitectureAnalyzer"]
        )

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(
            files_dict=files_dict, max_lines=None
        )  # max_lines=None per prendere tutto

        source_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] == "source" and f.get("confidence", 0) > 0.6
        }

        # 2. Integrare eventuali info dal contesto (moduli, namespaces, entry points)
        architecture_info = crew_context.get("CodeArchitectureAnalyzer", {})
        extra_info = {
            "modules": architecture_info.get("modules", []),
            "namespaces": architecture_info.get("namespaces", [])
        }

        files_b64 = to_b64(source_files)

        # 3. Prompt ottimizzato per estrazione API con input/output
        prompt = f"""
        You are a senior software architect and API reverse engineering LLM.

        You are given:

        - SOURCE FILES (base64): {files_b64}
        - PROJECT CONTEXT: {json.dumps(project_context, indent=2)}
        - CONTEXT INFO: {json.dumps(extra_info, indent=2)}

        Detect and categorize APIs, including detailed characterization of inputs and outputs:

        - internal APIs
        - public APIs
        - REST endpoints (paths, HTTP methods, input/output schema)
        - CLI commands (arguments, options, output)
        - RPC interfaces (method names, parameters, return types)
        - modules exposing APIs
        - namespaces involved
        - input/output parameters for all APIs
        - protocols, formats, serialization (JSON, XML, etc.)
        - expected errors and status codes

        Return STRICT JSON:

        {{
            "internal_apis":[],
            "public_apis":[],
            "rest_endpoints":[],
            "cli_commands":[],
            "rpc_interfaces":[],
            "api_modules":[],
            "api_namespaces":[],
            "api_io_characterization": []
        }}
        
        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed