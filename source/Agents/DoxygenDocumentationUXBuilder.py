import json
import os
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class DoxygenDocumentationUXBuilder(Agent):
    """
    Advanced Documentation UI/UX Architect using Doxygen data and full project analysis.

    Produces:
    - header.html
    - footer.html
    - stylesheet.css
    - index.html (landing page)
    - Secondary pages: API explorer, architecture, use cases, security, devops, quality, versioning
    - Updates Doxyfile if project analysis suggests optimizations
    - Fills content dynamically based on project data (tech stack, APIs, use cases, roles, diagrams)
    """

    def __init__(self):
        super().__init__(
            "DoxygenDocumentationUXBuilder",
            depends_on=[
                "DoxygenConfigBuilder",
                "ProjectMetadataAnalyzer",
                "MDDocumentationMaker",
                "UsageAnalyzer",
                "APIAnalyzer",
                "SecurityPermissionAnalyzer",
                "DevOpsAnalyzer",
                "VersioningAnalyzer",
                "QualityAnalyzer",
                "DocumentationAnalyzer"
            ]
        )

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        project_root = task.get("project_root", ".")
        doxyfile_path = os.path.join(project_root, "doxygen_custom", "Doxyfile")
        full_context = {k: crew_context.get(k, {}) for k in self.depends_on}
        context_json = json.dumps(full_context, indent=2)

        prompt = f"""
        You are a senior UI/UX architect and documentation engineer.
        Your goal is to generate a **fully populated interactive documentation website**
        based on all available project data.

        INPUTS:
        - Current Doxyfile path: {doxyfile_path}
        - Full project context (languages, toolchain, use cases, roles, protocols,
          versions, licenses, APIs, usage patterns, Markdown files):
        {context_json}

        TASK:
        1) Generate the full HTML documentation site:
           - index.html: hero section (project name, description, logo), badges (build, coverage, license), quick links (GitHub, MD docs)
           - Pages: API, architecture, use cases, security, devops, versioning, quality metrics
           - Navigation: topbar, sidebar, breadcrumbs, search form
           - Populate each page with actual project data, including:
             - Tech stack tables
             - Supported protocols
             - Modules and component relationships
             - Use cases and user roles
             - Internal and external links
             - Code examples from the project
             - Diagrams for architecture, sequence, flow
        2) Ensure visual consistency: modern theme, responsive layout, light/dark mode
        3) Review the existing Doxyfile:
           - Adjust INPUT paths if needed
           - Enable Markdown integration
           - Enable diagrams, call graphs, dependency graphs
           - Suggest any other optimizations
        4) Return updated Doxyfile if modified, and all populated HTML/CSS assets

        OUTPUT JSON:
        {{
            "updated_doxyfile": "...",
            "html_files": [
                {{"path": "header.html", "content": ""}},
                {{"path": "footer.html", "content": ""}},
                {{"path": "stylesheet.css", "content": ""}},
                {{"path": "index.html", "content": ""}},
                {{"path": "pages/api.html", "content": ""}},
                {{"path": "pages/architecture.html", "content": ""}},
                {{"path": "pages/usecases.html", "content": ""}},
                {{"path": "pages/security.html", "content": ""}},
                {{"path": "pages/devops.html", "content": ""}},
                {{"path": "pages/versioning.html", "content": ""}},
                {{"path": "pages/quality.html", "content": ""}}
            ],
            "ui_architecture": {{"pages": [], "navigation": {{}}, "user_flows": []}},
            "components": {{"tables": [], "charts": [], "diagrams": [], "cards": [], "forms": []}},
            "design_system": {{
                "theme": "modern",
                "dark_mode": true,
                "layout": "responsive",
                "typography": "professional"
            }}
        }}

        Return ONLY JSON.
        """

        result = llm_run(prompt, max_tokens=10000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}

        self.save_to_json(data=parsed, raw_content=result)

        # SAVE HTML FILES
        output_dir = os.path.join(project_root, "doxygen_ui")
        os.makedirs(output_dir, exist_ok=True)
        for f in parsed.get("html_files", []):
            fpath = os.path.join(output_dir, f["path"])
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as hfile:
                hfile.write(f["content"])

        # UPDATE Doxyfile if returned by LLM
        if "updated_doxyfile" in parsed:
            os.makedirs(os.path.dirname(doxyfile_path), exist_ok=True)
            with open(doxyfile_path, "w", encoding="utf-8") as f:
                f.write(parsed["updated_doxyfile"])

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed

