import json


from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, take_first_lines, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class SecurityPermissionAnalyzer(Agent):
    """
    Analizza sicurezza, permessi e modelli di autenticazione/autorizzazione.
    Integra informazioni di API, architettura e moduli.
    """

    def __init__(self):
        super().__init__("SecurityPermissionAnalyzer", depends_on=["APIAnalyzer", "CodeArchitectureAnalyzer", "ProjectTreeAnalyzer"])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "script"] and f.get("confidence", 0) > 0.6
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        # 2. Integra info da altri agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        architecture_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")

        prompt = f"""
        You are a security architecture analyst.

        Given the relevant project files (base64), API info, and architecture context:

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        FILES_B64:
        {files_b64}

        API_INFO:
        {json.dumps(api_info, indent=2)}

        ARCHITECTURE_INFO:
        {json.dumps(architecture_info, indent=2)}

        PROJECT_TREE:
        {json.dumps(project_tree, indent=2)}

        Detect and detail:

        - authentication methods (per module/namespace)
        - authorization models and permission levels
        - user roles and admin capabilities
        - sensitive operations
        - security mechanisms
        - secrets, keys, and credentials management

        Return STRICT JSON:

        {{
            "authentication_methods":[],
            "authorization_model":"",
            "user_roles":[],
            "admin_capabilities":[],
            "permission_model":"",
            "security_features":[],
            "secrets_management":[]
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=6000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed



