import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run, llm_run_safe




class DocumentationAnalyzer(Agent):
    """
    Advanced Documentation Analyzer (format-agnostic):
    - Identifica tutti i file documentali (Markdown, PDF, DOCX, XLSX, immagini, diagrammi)
    - Analizza struttura, root e collegamenti tra documenti
    - Rileva strumenti di documentazione e automazione
    - Collega documentazione alle entità di progetto (API, features, roles, actors, usecases)
    - Deduce qualità, completezza, aggiornamento e integrazione
    """

    def __init__(self):
        super().__init__(
            "DocumentationAnalyzer",
            depends_on=[
                "APIAnalyzer",
                "VersioningAnalyzer",
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

        file_catalog = [
            {"path": path, "type": path.split('.')[-1] if '.' in path else 'unknown', "size": len(content)}
            for path, content in files_dict.items()
        ]

        context_data = {
            "API_INFO": self.get_agent_output(crew_context, "APIAnalyzer"),
            "VERSIONING_INFO": self.get_agent_output(crew_context, "VersioningAnalyzer"),
            "SECURITY_INFO": self.get_agent_output(crew_context, "SecurityPermissionAnalyzer"),
            "DEVOPS_INFO": self.get_agent_output(crew_context, "DevOpsAnalyzer")
        }

        prompt = f"""
        You are an expert documentation engineer. Analyze the project structure and provide a structural JSON report.

        PROJECT CONTEXT: {json.dumps(project_context)}
        FILE CATALOG: {json.dumps(file_catalog)}
        DEPENDENCIES AND ARCHITECTURE: {json.dumps(context_data)}

        TASKS:
        1. Classify files in documentation vs other resources.
        2. Detect tools, readmes, and gaps.
        3. Map files to APIs, roles, and usecases.
        
        STRICT RULES:
        - Return ONLY raw JSON. No markdown backticks (```json).
        - If the file list is large, group files by directory/category instead of listing every single file to stay within token limits.
        - Ensure all JSON fields from the schema are filled.

        SCHEMA:
        {{
            "documentation_present": true,
            "root_documentation_file": "path/to/file",
            "documentation_files": [{{ "path": "...", "type": "...", "completeness": "full/partial/missing", "categories": [] }}],
            "documentation_tools_detected": [{{ "name": "...", "integration_ci_cd": true }}],
            "readme_present": true,
            "faq_present": false,
            "developer_guides": [],
            "api_documentation": [],
            "official_links": [],
            "contacts": null,
            "other_resources": [{{ "path": "...", "type": "..." }}]
        }}
        """

        # Usiamo llm_run_safe invece di llm_run semplice.
        # Questo abiliterà il chunking automatico se la risposta eccede il limite.
        result = llm_run_safe(
            prompt, 
            max_tokens=8000, 
            expect_json=True
        )

        if not result.ok:
            logger.error(f"[{self.name}] LLM failed: {result.error}")
            return {"error": "llm_failed", "raw": result.error}
        
        logger.info(f"[{self.name}] result: {result.data}")
        logger.info(f"[{self.name}] end running")
        return result.data
    


