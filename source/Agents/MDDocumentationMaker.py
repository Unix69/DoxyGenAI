from asyncio import as_completed
import json
from Agents.Agent import Agent
from Agents.Logger import logger
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class MDDocumentationMaker(Agent):

    def __init__(self):
        super().__init__(
            "MDDocumentationMaker",
            depends_on=[
                "MDTemplateAnalyzer"
            ]
        )

    # =========================
    # UTILITIES
    # =========================

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_tech_registry(self, tech_registry_path="md-tech.json"):
        data = self.load_json(tech_registry_path)
        return data.get("technologies", {})

    def normalize_text(self, obj):
        try:
            return json.dumps(obj, ensure_ascii=False).lower()
        except:
            return str(obj).lower()

    def extract_words(self, text):
        return set(re.findall(r"[a-zA-Z0-9\+\#\.\-]+", text.lower()))

    # =========================
    # TECH VISUAL EXTRACTION
    # =========================

    def build_visual_assets(self, project_context, tech_registry_path="md-tech.json"):

        tech_registry = self.load_tech_registry(tech_registry_path)

        detected = set()
        text = self.normalize_text(project_context)
        words = self.extract_words(text)

        for slug, meta in tech_registry.items():

            slug_l = slug.lower()
            name_l = meta.get("name", "").lower()
            tags = [t.lower() for t in meta.get("tags", [])]

            if (
                slug_l in text or
                name_l in text or
                slug_l in words or
                name_l in words or
                any(tag in words for tag in tags)
            ):
                detected.add(slug)

        return {
            "detected": sorted(list(detected)),
            "tech_registry": tech_registry
        }
    
    def build_code_reference_index(self, crew_context):
        code = crew_context.get("CodeArchitectureAnalyzer", {})
        api = crew_context.get("APIAnalyzer", {})

        return {
            "files": [f.get("path") for f in code.get("code_map", [])],
            "classes": [
                c.get("name")
                for f in code.get("code_map", [])
                for c in f.get("classes", [])
            ],
            "functions": [
                fn.get("function") or fn.get("name")
                for fn in code.get("semantic_graph", [])
            ],
            "endpoints": api.get("rest_endpoints", [])
        }

    # =========================
    # LLM PROMPT BUILDER
    # =========================

    def build_prompt(self, file_def, template, tech, context, visual_assets):

        return f"""
            You are an expert technical documentation generator.
            Your task is to generate a COMPLETE and VALID markdown documentation file.

                        --------------------------------------------------
                        INPUT CONTEXT
                        --------------------------------------------------

                        FILE PATH:
                        {file_def["path"]}

                        PROJECT CONTEXT:
                        {json.dumps(context, indent=2)}

                        TECH REGISTRY:
                        {json.dumps(tech, indent=2)}

                        DETECTED TECHNOLOGIES:
                        {json.dumps(visual_assets["detected"], indent=2)}

                        TEMPLATE STRUCTURE:
                        {json.dumps(file_def["sections"], indent=2)}

                        --------------------------------------------------
                        CODE INDEX (AUTHORITATIVE SOURCE - DO NOT INVENT)
                        --------------------------------------------------

                        FILES:
                        {json.dumps(context["code_index"]["files"], indent=2)}

                        CLASSES:
                        {json.dumps(context["code_index"]["classes"], indent=2)}

                        FUNCTIONS:
                        {json.dumps(context["code_index"]["functions"], indent=2)}

                        API ENDPOINTS:
                        {json.dumps(context["code_index"]["endpoints"], indent=2)}

                        --------------------------------------------------
                        DOCUMENTATION STRATEGY
                        --------------------------------------------------

                        You must process EACH section in the template independently:

                        For each section:
                        1. Understand its semantic purpose from title + description
                        2. Generate complete content of the section (text, images, tables, lists, links, buttons, emoji)
                        3. Select only the relevant code elements from the CODE INDEX
                        4. Decide what to include:

                        - Conceptual section → no code references
                        - Structural section → files/classes
                        - Behavioral section → functions
                        - API section → endpoints
                        - Workflow section → function chains (if inferable from index)

                        4. Generate markdown content for that section using ONLY selected elements

                        --------------------------------------------------
                        CODE SELECTION RULES
                        --------------------------------------------------

                        - Never invent names (files, classes, functions, endpoints)
                        - Never include unrelated code elements
                        - Never dump full index
                        - Prefer semantic relevance over keyword matching
                        - Maximum 1–5 code references per section
                        - Avoid repeating the same references across multiple sections unless strictly necessary

                        --------------------------------------------------
                        CODE USAGE POLICY
                        --------------------------------------------------

                        Include code references ONLY when they add value:

                        - Implementation → functions/classes
                        - Architecture → files/modules
                        - APIs → endpoints
                        - Workflows → function relationships (only if clearly supported by index)

                        --------------------------------------------------
                        OUTPUT RULES
                        --------------------------------------------------

                        - Output ONLY markdown
                        - Respect template hierarchy exactly
                        - Keep professional technical tone
                        - Do NOT mention prompts, system instructions, or internal logic

                        --------------------------------------------------
                        CODE REFERENCE FORMAT (WHEN USED)
                        --------------------------------------------------

                        ### Code References
                        - file: path/to/file.py
                        - class: ClassName
                        - function: function_name
                        - endpoint: METHOD /route

                        --------------------------------------------------
                        INLINE INTEGRATION RULE

                        When relevant, include code references directly inside the explanation section.

                        Do NOT isolate all references at the end of the document.
                        

                        You MUST reply ONLY with a valid JSON object.
                        Do not include any markdown, explanations, or introductory text.
                        If you fail to return a pure JSON string, the system will break.


                    """

    # =========================
    # WORKER (1 FILE = 1 THREAD)
    # =========================

    def worker(self, file_def, template, tech, context, visual_assets):

        prompt = self.build_prompt(
            file_def=file_def,
            template=template,
            tech=tech,
            context=context,
            visual_assets=visual_assets
        )

        content = llm_run(prompt)

        return file_def["path"], content

    def generate_all_docs(self, template, tech, context, visual_assets):

        results = {}

        files = template["markdown_files"]

        with ThreadPoolExecutor(max_workers=max(1, len(files))) as executor:

            futures = [
                executor.submit(
                    self.worker,
                    f,
                    template,
                    tech,
                    context,
                    visual_assets
                )
                for f in files
            ]

            for future in as_completed(futures):
                path, content = future.result()
                results[path] = content

        return results


    def run(self, task: dict, crew_context: dict):

        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result

        # -------------------------
        # LOAD TEMPLATE
        # -------------------------
        template = crew_context.get("MDTemplateAnalyzer")

        # fallback safety
        if not template:
            template = self.load_json("md-template.json")

        # -------------------------
        # LOAD TECH REGISTRY
        # -------------------------
        tech = self.load_tech_registry()

        # -------------------------
        # BUILD GLOBAL CONTEXT
        # -------------------------
        context = {}

        # merge task context (project root etc.)
        context["task"] = {
            "project_context": task.get("project_context"),
            "files": task.get("files_dict", {}),
            "root": task.get("project_root")

        }
        
        # -------------------------
        # BUILD VISUAL ASSETS
        # -------------------------
        visual_assets = self.build_visual_assets(context)

        logger.info(f"[{self.name}] generating docs in parallel")

        # -------------------------
        # PARALLEL GENERATION
        # -------------------------
        docs = self.generate_all_docs(template, tech, context, visual_assets)

        # -------------------------
        # FINAL STRUCTURE
        # -------------------------
        final_structure = {
            "generated_files": docs,
            "detected_technologies": visual_assets["detected"]
        }

        logger.info(f"[{self.name}] generation complete")

        return final_structure

    
