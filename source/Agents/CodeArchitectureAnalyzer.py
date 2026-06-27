import json
from Agents.Logger import logger
from Agents.Agent import Agent
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.LLM import llm_run


class CodeArchitectureAnalyzer(Agent):

    def __init__(self):
        super().__init__("CodeArchitectureAnalyzer")

    
    @staticmethod
    def find_relevant_code(section_name, repo_ast, code_graph):

        prompt = f"""
        You are mapping documentation sections to source code.

        SECTION:
        {section_name}

        AVAILABLE CODE GRAPH:
        {json.dumps(code_graph, indent=2)}

        TASK:

        Find ONLY relevant code entities for this documentation section.

        Prefer:
        - semantic similarity
        - exact naming
        - architectural relevance
        - usage importance

        Return STRICT JSON:

        {{
            "functions": [],
            "classes": [],
            "files": [],
            "confidence": 0.0,
            "coverage": "none|partial|good|full",
            "ranking": [],
            "reasoning": ""
        }}

        You MUST reply ONLY with a valid JSON object.
        Do not include any markdown, explanations, or introductory text.
        If you fail to return a pure JSON string, the system will break.

        """

        result = llm_run(prompt, max_tokens=10000)

        parsed = extract_json(result)

        if not parsed:
            return {
                "functions": [],
                "classes": [],
                "files": [],
                "confidence": 0.0,
                "coverage": "none",
                "ranking": [],
                "reasoning": "No valid binding"
            }

        return parsed

    def extract_doc_targets(code_info):

        semantic = code_info.get("semantic_graph", [])
        calls = code_info.get("call_graph", [])
        code_map = code_info.get("code_map", [])

        targets = {
            "api": [],
            "classes": [],
            "services": [],
            "cli": [],
            "flows": [],
            "core_functions": []
        }

        for node in semantic:

            name = node.get("name", "").lower()
            typ = node.get("type", "").lower()

            if "route" in typ or "endpoint" in typ:
                targets["api"].append(node)

            elif "class" in typ:
                targets["classes"].append(node)

            elif "service" in name:
                targets["services"].append(node)

            elif "command" in name or "cli" in name:
                targets["cli"].append(node)

            elif "function" in typ:
                targets["core_functions"].append(node)

        # flow importanti
        for edge in calls[:30]:
            targets["flows"].append(edge)

        return targets

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] start running")
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result
        
         # 1. Recupera i dati di input dal task
        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})
        file_classifier = get_file_classifier()
        classified_files = file_classifier.classify_files_batch(
            files_dict=files_dict,
            max_lines=80
        )

        relevant_files = {
            f["path"]: task["files_dict"][f["path"]]
            for f in classified_files
            if f["type"] in ["source", "config"]
        }

        files_b64 = to_b64(relevant_files)

        prompt = f"""
            You are a senior software architect performing deep reverse engineering.

            You must extract BOTH:
            1. SYSTEM ARCHITECTURE (high level)
            2. CODE STRUCTURE + SEMANTIC MODEL (low level)

            PROJECT CONTEXT: {json.dumps(project_context, indent=2)}

            --------------------------------------------------
            INPUT FILES
            --------------------------------------------------
            FILES_B64:
            {files_b64}

            --------------------------------------------------
            TASK
            --------------------------------------------------

            Analyze the codebase and extract:

            ## 1. ARCHITECTURE LAYER
            - architecture_style
            - architectural_patterns
            - major_components
            - modules
            - layering
            - coupling_level
            - cohesion_level
            - entry_points
            - dependency_direction

            ## 2. CODE STRUCTURE LAYER (IMPORTANT)
            For each file, extract:

            - file path
            - classes
            - functions
            - methods
            - imports
            - responsibilities

            ## 3. SEMANTIC FUNCTION GRAPH (CRITICAL)
            For each function:

            - name
            - file
            - inputs
            - outputs
            - purpose
            - calls (internal dependencies)
            - side effects (db, api, io)
            - role (api handler, service, utility, etc.)

            ## 4. CALL RELATIONSHIPS
            Extract function-to-function relationships:
            - caller → callee graph edges

            --------------------------------------------------
            OUTPUT FORMAT (STRICT JSON)
            --------------------------------------------------

            {{
            "architecture": {{
                "architecture_style": "",
                "architectural_patterns": [],
                "major_components": [],
                "modules": [],
                "layering": [],
                "coupling_level": "",
                "cohesion_level": "",
                "entry_points": [],
                "dependency_direction": ""
            }},

            "code_map": [
                {{
                "path": "",
                "classes": [
                    {{
                    "name": "",
                    "methods": []
                    }}
                ],
                "functions": [],
                "imports": [],
                "responsibility": ""
                }}
            ],

            "semantic_graph": [
                {{
                "function": "",
                "file": "",
                "inputs": [],
                "outputs": [],
                "purpose": "",
                "calls": [],
                "side_effects": [],
                "role": ""
                }}
            ],

            "call_graph": [
                {{
                "from": "",
                "to": ""
                }}
            ]
            }}

            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            --------------------------------------------------
            RULES
            --------------------------------------------------

            - Do NOT hallucinate functions that do not exist
            - Prefer explicit code evidence over inference
            - If uncertain, mark field as "unknown"
            - Keep structure consistent across files
            """

        result = llm_run(prompt, max_tokens=3000)
        parsed = extract_json(result) or {"error": "invalid_json", "raw": result}
        self.save_to_json(data=parsed, raw_content=result)
        

        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return parsed
