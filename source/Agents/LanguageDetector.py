import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, take_first_lines, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run

class LanguageDetector(Agent):

    def __init__(self):
        super().__init__("LanguageDetector")

    def run(self, task, crew_context):

        logger.info(f"[{self.name}] start running")
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        
        # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # ----------------------------
        # 2. Estensioni file (veloce)
        # ----------------------------
        file_extensions = list({
            path.split(".")[-1].lower()
            for path in files_dict.keys()
            if "." in path
        })

        # ----------------------------
        # 3. Sampling contenuto
        # ----------------------------
        sampled_files = take_first_lines(files_dict, 50)
        sampled_b64 = to_b64(sampled_files)

        # ----------------------------
        # PROMPT OTTIMIZZATO
        # ----------------------------
        prompt = f"""
            You are a programming language detection engine.

            You are given:

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            FILE EXTENSIONS:
            {file_extensions}

            SAMPLE FILE CONTENTS (first lines only, base64):
            {sampled_b64}

            Detect:

            - primary_language
            - secondary_languages
            - scripting_languages
            - configuration_languages
            - markup_languages
            - language_standards (C11, C++17, Python3, etc)
            - multi_language_project
            - interpreted_or_compiled
            - codebase_size_estimate

            Return STRICT JSON:

            {{
            "primary_language": "",
            "secondary_languages": [],
            "scripting_languages": [],
            "configuration_languages": [],
            "markup_languages": [],
            "language_standards": {{}},
            "multi_language_project": true,
            "interpreted_or_compiled": "",
            "codebase_size_estimate": "",
            "confidence": 0.0
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            Return null where unknown.
        """

        result = llm_run(prompt, max_tokens=2000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}
        self.save_to_json(data=parsed, raw_content=result)
        
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed