import json
from Agents.Agent import Agent
from Agents.Logger import logger
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run

class ProjectMetadataAnalyzer(Agent):
    """
    Analizza tutti i dati prodotti dagli altri agenti e genera un metadata esaustivo del progetto,
    integrando info su linguaggi, dipendenze, architettura, API, uso, sicurezza, DevOps, 
    documentazione, versioning e qualità.
    """

    def __init__(self):
        super().__init__(
            "ProjectMetadataAnalyzer",
            depends_on=[
                "LanguageDetector",
                "DependencyDetector",
                "CodeArchitectureAnalyzer",
                "APIAnalyzer",
                "UsageAnalyzer",
                "DevOpsAnalyzer",
                "SecurityPermissionAnalyzer",
                "DocumentationAnalyzer",
                "VersioningAnalyzer",
                "QualityAnalyzer",
                "ProjectTreeAnalyzer",
                "BuildSystemDetector"
            ]
        )

    def run(self, task, crew_context):
        # Costruzione del contesto completo
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        context_info = {agent: self.get_agent_output(crew_context, agent) for agent in self.depends_on}
        project_context = self.get_task(task, "project_context", {})

        prompt = f"""
        You are a senior software project analyst and documentation generator.

        Using the full context of previous analyses, generate a comprehensive project metadata report.

        PROJECT_CONTEXT:

        {json.dumps(project_context, indent=2)}

        CONTEXT_INFO:
        
        {json.dumps(context_info, indent=2)}

        Infer:

        - project_description
        - goal
        - targets
        - benefits
        - risks
        - techstack
        - architecture_summary
        - features
        - settings
        - APIs
        - namespaces
        - modules
        - entry_points
        - directory_structure
        - build_systems
        - ci_cd
        - containerization
        - deployment_targets
        - security_summary
        - authentication_methods
        - authorization_models
        - user_roles
        - admin_capabilities
        - sensitive_operations
        - secrets_management
        - documentation_summary
        - documentation_tools
        - documentation_coverage
        - versioning_summary
        - release_history
        - changelog
        - technical_debt
        - code_quality
        - test_quality
        - performance_quality
        - service_quality
        - risk_level
        - traceability

        Return STRICT JSON with all fields populated. Use null if unknown.

        {{
            "project_description":"",
            "goal":"",
            "targets":[],
            "benefits":[],
            "risks":[],
            "techstack":[],
            "architecture_summary":"",
            "features":[],
            "settings":[],
            "apis":[],
            "namespaces":[],
            "modules":[],
            "entry_points":[],
            "directory_structure":{{}},
            "build_systems":[],
            "ci_cd":[],
            "containerization":[],
            "deployment_targets":[],
            "security_summary":{{}},
            "authentication_methods":[],
            "authorization_models":[],
            "user_roles":[],
            "admin_capabilities":[],
            "sensitive_operations":[],
            "secrets_management":[],
            "documentation_summary":{{}},
            "documentation_tools":[],
            "documentation_coverage":{{}},
            "versioning_summary":{{}},
            "release_history":[],
            "changelog_present":true,
            "technical_debt":{{}},
            "code_quality":{{}},
            "test_quality":{{}},
            "performance_quality":{{}},
            "service_quality":{{}},
            "risk_level":"",
            "traceability":{{}}
        }}
        
        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=4000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

