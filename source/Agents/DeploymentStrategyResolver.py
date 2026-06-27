import json
from typing import Any, Dict
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run



class DeploymentStrategyResolver(Agent):
    """
    Resolves and validates deployment strategy from user preferences.
    Deterministic, strict validation.
    """

    def __init__(self):
        super().__init__("DeploymentStrategyResolver", depends_on=[])

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        prefs = task.get("deployment_preferences", {})

        if not prefs:
            raise ValueError("deployment_preferences is required")

        strategy = {
            "type": prefs.get("type"),
            "platform": prefs.get("platform"),
            "branch": prefs.get("branch", "main"),
            "docs_path": prefs.get("docs_path", "docs"),
            "custom_domain": prefs.get("custom_domain"),
            "docker_image": prefs.get("docker_image"),      # container
            "k8s_namespace": prefs.get("k8s_namespace"),    # kubernetes
            "server_user": prefs.get("server_user"),        # server
            "cloud_bucket": prefs.get("cloud_bucket")       # cloud
        }

        valid_types = ["static", "container", "kubernetes", "server", "cloud"]

        valid_platforms = {
            "static": ["github_pages", "gitlab_pages", "netlify", "vercel", "s3"],
            "container": ["docker"],
            "kubernetes": ["k8s"],
            "server": ["nginx", "apache"],
            "cloud": ["s3", "cloudfront"]
        }

        # ----------------------------
        # VALIDATION
        # ----------------------------
        if strategy["type"] not in valid_types:
            raise ValueError(f"Invalid deployment type: {strategy['type']}")

        if strategy["platform"] not in valid_platforms.get(strategy["type"], []):
            raise ValueError(
                f"Incompatible platform '{strategy['platform']}' for type '{strategy['type']}'"
            )

        crew_context[self.name] = strategy
        return strategy

class DocumentationDeploymentGenerator(Agent):
    """
    Production-grade deployment generator for documentation systems.
    LLM-driven but strictly constrained.
    """

    def __init__(self):
        super().__init__(
            "DocumentationDeploymentGenerator",
            depends_on=[
                "DeploymentStrategyResolver",
                "DoxygenConfigBuilder",
                "DoxygenDocumentationUXBuilder",
                "DevOpsAnalyzer",
                "ProjectMetadataAnalyzer"
            ]
        )

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]):

        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result

        project_root = task.get("project_root", ".")
        strategy = crew_context.get("DeploymentStrategyResolver")

        if not strategy:
            raise RuntimeError("Deployment strategy not resolved")

        context = {k: crew_context.get(k, {}) for k in self.depends_on}

        prompt = f"""
            You are a senior DevOps engineer specialized in documentation systems.

            ==================================================
            DEPLOYMENT STRATEGY (STRICT INPUT):
            {json.dumps(strategy, indent=2)}

            FULL PROJECT CONTEXT:
            {json.dumps(context, indent=2)}

            ==================================================
            MANDATORY RULES:

            - DO NOT infer anything
            - DO NOT change strategy
            - DO NOT ask questions
            - FOLLOW strategy strictly

            ==================================================
            GLOBAL REQUIREMENTS:

            1. Build system:
            - Provide build_docs.sh (bash)
            - Must be idempotent
            - Must fail on error (set -e)

            2. Doxygen:
            - Execute using provided config
            - Respect OUTPUT_DIRECTORY from config
            - Integrate Markdown
            - Include diagrams if available

            3. Post-processing:
            - Copy UI assets
            - Fix relative paths
            - Ensure deploy-ready structure

            4. Output:
            - Use correct output directory from Doxygen
            - Ensure static hosting compatibility

            ==================================================
            CI/CD REQUIREMENTS (MANDATORY):

            - Install dependencies (doxygen, graphviz, etc.)
            - Use caching if possible
            - Upload artifacts
            - Restrict to main/master branch
            - Use production-ready actions/templates

            ==================================================
            TYPE-SPECIFIC REQUIREMENTS:

            ### STATIC:

            Platform-specific behavior:
            - github_pages → .github/workflows/docs.yml
            - gitlab_pages → .gitlab-ci.yml
            - netlify/vercel → config files

            Must:
            - deploy generated HTML
            - handle base path issues

            ### CONTAINER:

            Must generate:
            - Dockerfile (multi-stage)
            - docker-compose.yml

            Dockerfile MUST:
            - use nginx:alpine
            - copy only built docs
            - expose port 80

            ### KUBERNETES:

            Must generate:
            - deployment.yaml
            - service.yaml
            - ingress.yaml

            Use:
            - nginx container
            - proper labels/selectors

            ### SERVER:

            Must generate:
            - deploy.sh (scp + ssh)
            - nginx.conf

            ### CLOUD (S3):

            Must generate:
            - deploy script using aws cli
            - sync command
            - optional cloudfront invalidation

            ==================================================
            OUTPUT FORMAT (STRICT JSON):

            {{
            "files": [
                {{
                "path": "",
                "content": ""
                }}
            ]
            }}

            Return ONLY JSON.
            """

        result = llm_run(prompt, max_tokens=6000)
        parsed = extract_json(result)

        # ----------------------------
        # VALIDATION
        # ----------------------------
        if not parsed or "files" not in parsed:
            raise RuntimeError("Invalid deployment generation output")

        # ----------------------------
        # WRITE FILES
        # ----------------------------
        for f in parsed["files"]:
            path = os.path.join(project_root, f["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)

            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(f["content"])
            except Exception as e:
                logger.error(f"Error writing {path}: {e}")

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed
