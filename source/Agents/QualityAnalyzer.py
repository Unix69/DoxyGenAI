    
import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run
 


class QualityAnalyzer(Agent):
    """
    Analizza il progetto software e produce metriche quantitative per codice, test, sicurezza,
    performance, documentazione, servizio, scalabilità, affidabilità e technical debt.

    Integra informazioni dagli altri agenti:
    - ProjectTreeAnalyzer
    - LanguageDetector
    - BuildSystemDetector
    - DependencyDetector
    - CodeArchitectureAnalyzer
    - APIAnalyzer
    - UsageAnalyzer
    - SecurityPermissionAnalyzer
    - DevOpsAnalyzer
    - DocumentationAnalyzer
    - VersioningAnalyzer
    """

    def __init__(self):
        super().__init__("QualityAnalyzer", depends_on=[
            "ProjectTreeAnalyzer",
            "LanguageDetector",
            "BuildSystemDetector",
            "DependencyDetector",
            "CodeArchitectureAnalyzer",
            "APIAnalyzer",
            "UsageAnalyzer",
            "SecurityPermissionAnalyzer",
            "DevOpsAnalyzer",
            "DocumentationAnalyzer",
            "VersioningAnalyzer"
        ])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # ----------------------------
        # 1. Filtraggio file rilevanti
        # ----------------------------

        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(files_dict=files_dict, max_lines=50)
        relevant_files = {
            f["path"]: files_dict[f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config", "script"]
        }
        files_b64 = to_b64(relevant_files)

        # ----------------------------
        # 2. Raccolta informazioni dagli altri agenti
        # ----------------------------
        context_info = {agent: self.get_agent_output(crew_context, agent) for agent in self.depends_on}

        # ----------------------------
        # 3. Prompt LLM per analisi avanzata quantitativa
        # ----------------------------
        prompt = f"""
        You are an expert software quality and metrics analyst.

        Analyze the software project in depth using the given files (base64) and context info
        from other agents.

        FILES_B64:
        {files_b64}

        PROJECT CONTEXT:
        {json.dumps(project_context, indent=2)}

        CONTEXT_INFO:
        {json.dumps(context_info, indent=2)}

        For the project, generate quantitative and qualitative metrics across these dimensions:

        1. CODE QUALITY:
           - maintainability (score 0-10)
           - cohesion and coupling (score 0-10)
           - code complexity per module (cyclomatic complexity, function/method size)
           - coding standard adherence (%)
           - potential bugs and code smells (list + severity)
           - multi-language consistency

        2. TEST QUALITY:
           - test coverage per module (%)
           - completeness of unit, integration, and e2e tests
           - gaps or missing test scenarios
           - reliability of test executions

        3. DOCUMENTATION QUALITY:
           - completeness, clarity, and consistency
           - traceability to APIs, modules, use cases
           - presence of documentation automation tools (Doxygen, Sphinx, MkDocs, etc.)
           - type and structure of documentation (PDF, DOCX, Markdown, HTML, images)

        4. SECURITY:
           - coverage of authentication/authorization
           - secrets, keys, credentials management
           - known vulnerability patterns
           - security score 0-10

        5. PERFORMANCE & SCALABILITY:
           - estimated efficiency of code
           - potential bottlenecks
           - scalability potential
           - parallelization, caching, database access
           - performance score 0-10

        6. SERVICE & RELIABILITY:
           - CI/CD pipeline quality
           - deployment robustness
           - monitoring and logging completeness
           - fault tolerance, availability, disaster recovery
           - reliability score 0-10

        7. DEPENDENCIES & DEVOPS:
           - dependency management quality
           - versioning hygiene
           - containerization/orchestration quality
           - deployment and environment risks

        8. TECHNICAL DEBT & RISKS:
           - estimated technical debt (score 0-10)
           - risk assessment (low/medium/high)
           - traceability of features, APIs, modules, versions, use cases
           - criticality mapping

        Return STRICT JSON with these fields:

        {{
            "code_quality": {{"score":0, "metrics":{{}}, "potential_bugs":[]}},
            "test_quality": {{"coverage":0, "gaps":[], "reliability_score":0}},
            "documentation_quality": {{"score":0, "tools":[],"formats":[],"traceability":{{}}}},
            "security_quality": {{"score":0, "issues":[]}},
            "performance_quality": {{"score":0, "bottlenecks":[], "scalability_score":0}},
            "service_quality": {{"score":0, "ci_cd_score":0, "monitoring":[], "availability_score":0}},
            "technical_debt": {{"score":0, "critical_modules":[]}},
            "risk_level": "",
            "traceability": {{}}
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        # ----------------------------
        # 4. Esecuzione LLM
        # ----------------------------
        result = llm_run(prompt, max_tokens=6000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        # ----------------------------
        # 5. Salvataggio nel contesto
        # ----------------------------
        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed