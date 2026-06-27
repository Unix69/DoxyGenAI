import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, take_first_lines, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class VersioningAnalyzer(Agent):
    """
    Analizza il versioning del software e tiene traccia delle entità per versione:
    - features, APIs, namespaces, roles, actors, usecases
    - change, bug, fix
    - timestamp e release history
    """

    def __init__(self):
        super().__init__(
            "VersioningAnalyzer",
            depends_on=[
                "APIAnalyzer",
                "ProjectTreeAnalyzer",
                "SecurityPermissionAnalyzer",
                "DevOpsAnalyzer"
            ]
        )

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=100)


        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "changelog", "script"] and f.get("confidence", 0) > 0.6
        }

        snippets = take_first_lines(relevant_files, 100)
        files_b64 = to_b64(snippets)

        # Integra informazioni dagli altri agenti
        api_info = self.get_agent_output(crew_context, "APIAnalyzer")
        security_info = self.get_agent_output(crew_context, "SecurityAnalyzer")
        devops_info = self.get_agent_output(crew_context, "DevOpsAnalyzer")
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")

        prompt = f"""
        You are a software versioning and release historian.

        Given the project files (base64), APIs, features, project tree, security, and DevOps context:

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        FILES_B64:
        {files_b64}

        API_INFO:
        {json.dumps(api_info, indent=2)}

        PROJECT_TREE:
        {json.dumps(project_tree, indent=2)}

        SECURITY_INFO:
        {json.dumps(security_info, indent=2)}

        DEVOPS_INFO:
        {json.dumps(devops_info, indent=2)}

        Detect and produce a structured timeline including:

        - version releases with timestamp
        - for each version:
            - APIs, namespaces, features, roles, actors, usecases
            - for each entity, include 'introduced_in_version' and 'last_modified_version'
        - all changes, bug reports, fixes with timestamps
        - link each change/bug/fix to affected APIs, namespaces, features, roles, actors, usecases, indicating the version for each
        - version control system, semantic versioning, changelog, release notes
        - git workflow, pull request templates, issue templates

        Return STRICT JSON:

        {{
            "versioning_system":"",
            "semantic_versioning":true,
            "git_workflow":"",
            "changelog_present":true,
            "release_notes_present":true,
            "pull_request_templates":true,
            "issue_templates":true,
            "versions":[
                {{
                    "version":"",
                    "release_date":"",
                    "apis":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "namespaces":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "features":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "roles":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "actors":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "usecases":[{{"name":"","introduced_in_version":"","last_modified_version":""}}],
                    "changes":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ],
                    "bugs":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ],
                    "fixes":[
                        {{
                            "description":"",
                            "timestamp":"",
                            "affected_apis":[],
                            "affected_features":[],
                            "affected_roles":[],
                            "affected_actors":[],
                            "affected_usecases":[]
                        }}
                    ]
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