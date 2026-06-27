import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, take_first_lines, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class BuildSystemDetector(Agent):

    def __init__(self):
        super().__init__("BuildSystemDetector")

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        
        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        if not files_dict:
            result = {"error": "no_files"}
            crew_context[self.name] = result
            return result

        # ----------------------------
        # STEP 1: PREFILTER (cheap)
        # ----------------------------
        filtered_files = prefilter_files(files_dict)

        # fallback sicurezza
        if not filtered_files:
            filtered_files = files_dict


        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(filtered_files, max_lines=50)

        # Step 3: estrarre solo file rilevanti per build/dependency/config
        build_candidates = {
            f["path"]: filtered_files[f["path"]]
            for f in classified_files
            if f["type"] in ["build", "dependency", "config", "ci_cd", "container"] and f.get("confidence", 0) > 0.5
        }

        # fallback se vuoto
        if not build_candidates:
            build_candidates = filtered_files

        snippets = take_first_lines(build_candidates, 200)
        files_b64 = to_b64(snippets)

        # ----------------------------
        # STEP 4: ANALISI BUILD SYSTEM
        # ----------------------------
        prompt = f"""
        You are an expert build systems analyzer.

        PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

        FILES_B64 contains relevant build/configuration files.

        {files_b64}

        Detect:

        - build_systems
        - build_files
        - build_commands
        - test_commands
        - package_managers
        - ci_cd_detected
        - containerization
        - build_complexity
        - cross_platform_support

        Return JSON:

        {{
            "build_systems": [],
            "build_files": [],
            "build_commands": [],
            "test_commands": [],
            "package_managers": [],
            "ci_cd_detected": [],
            "containerization": [],
            "build_complexity": "",
            "cross_platform_support": true
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.


        """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}
        self.save_to_json(data=parsed, raw_content=result)

        # ----------------------------
        # DEBUG INFO (OPZIONALE)
        # ----------------------------
        parsed["_meta"] = {
            "total_files": len(files_dict),
            "filtered_files": len(filtered_files),
            "build_candidates": len(build_candidates)
        }

        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed