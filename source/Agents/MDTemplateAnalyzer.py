import json
from Agents.Agent import Agent
from Agents.CodeArchitectureAnalyzer import CodeArchitectureAnalyzer
from Agents.Logger import logger
from Agents.Tools import GitHubManager
from Agents.Tools.Tools import extract_json, to_b64
from Agents.Tools.FileClassifier import get_file_classifier
from Agents.Tools.GitHubManager import MarkdownElementExtractor
from Agents.Tools.LLM import llm_run


class MDTemplateAnalyzer(Agent):

    def __init__(self):
        super().__init__("MDTemplateAnalyzer", depends_on=[
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
                "BuildSystemDetector",
                "ProjectMetadataAnalyzer"
            ])

        with open("./Agents/md-template.json", "r", encoding="utf-8") as f:
            self.base_template = json.load(f)

    def run(self, task: dict, crew_context: dict):
        
        logger.info(f"[{self.name}] start running") 
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result

        github_token = self.get_task(task, "github_token", "")
        github_username = self.get_task(task, "github_username", "")
        

        files_dict = self.get_task(task, "files_dict", {})
        project_context = self.get_task(task, "project_context", {})

        # -------------------------------------------------
        # 1. GitHub Manager
        # -------------------------------------------------
        gh = GitHubManager(
            github_token=github_token,
            username=github_username
        )

        # -------------------------------------------------
        # 2. Repo passate da input / altri agenti
        # -------------------------------------------------
        input_repos = self.get_task(task, "repos", [])

        logger.info(f"[{self.name}] input repos: {len(input_repos)}")
        logger.info(json.dumps(input_repos, indent=2))

        # -------------------------------------------------
        # 3. Repo trovate automaticamente simili al progetto
        # -------------------------------------------------
        discovered_repos = []

        try:
            discovered_repos = gh.discover_repos_from_context(
                crew_context,
                max_repos=1
            )

            logger.info(
                f"[{self.name}] auto discovered repos: {len(discovered_repos)}"
            )
            logger.info(json.dumps(discovered_repos, indent=2))

        except Exception as e:
            logger.warning(
                f"[{self.name}] discover_repos_from_context failed: {e}"
            )

        # -------------------------------------------------
        # 4. Repo user personali (opzionale)
        # -------------------------------------------------
        user_repos = []

        try:
            if github_username:
                user_repos = gh.get_user_repos(max_repos=1)

                logger.info(
                    f"[{self.name}] user repos found: {len(user_repos)}"
                )
                logger.info(json.dumps(user_repos, indent=2))

        except Exception as e:
            logger.warning(
                f"[{self.name}] get_user_repos failed: {e}"
            )

        # -------------------------------------------------
        # 5. Merge intelligente finale
        # -------------------------------------------------
        repos = GitHubManager.merge_repos(
            input_repos,
            discovered_repos,
            user_repos,
            max_total=8
        )

        logger.info(
            f"[{self.name}] final repos to analyze: {len(repos)}"
        )
        logger.info(json.dumps(repos, indent=2))

        # Salva per debug nel context
        crew_context["repos"] = repos

        # -------------------------------------------------
        # 6. Recupera dati progetto
        # -------------------------------------------------
        project_tree = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        language_info = self.get_agent_output(crew_context, "LanguageDetector")
        build_info = self.get_agent_output(crew_context, "BuildSystemDetector")
        usage_info = self.get_agent_output(crew_context, "UsageAnalyzer")
        
        # Estraiamo i grafi e le mappe direttamente dal dizionario di CodeArchitectureAnalyzer
        code_info = self.get_agent_output(crew_context, "CodeArchitectureAnalyzer")
        code_graph = code_info.get("semantic_graph", [])
        call_graph = code_info.get("call_graph", [])
        code_map = code_info.get("code_map", [])
        doc_targets = CodeArchitectureAnalyzer.extract_doc_targets(code_info)
        
        quality_info = self.get_agent_output(crew_context, "QualityAnalyzer")

        

        # -------------------------------------------------
        # 7. Analizza repo markdown (STRUTTURALE + AST)
        # -------------------------------------------------
        extractor = MarkdownElementExtractor()
        repo_structures = {}

        for repo_info in repos:

            owner = repo_info["owner"]
            repo = repo_info["repo"]

            logger.info(f"\n[{self.name}] analyzing repo: {owner}/{repo}")

            try:
                md_files = gh.fetch_repo_md_files(
                    owner=owner,
                    repo=repo
                )

                logger.info(f"[{self.name}] markdown files found: {len(md_files)}")

                parsed_files = {}

                # -------------------------------------------------
                # 1. PARSING COMPLETO DI OGNI FILE MD
                # -------------------------------------------------
                for path, content in md_files.items():
                    parsed_files[path] = extractor.parse(content, file_path=path)

                repo_ast = {
                    "files": parsed_files,
                    "global_headings": [],
                    "global_tables": [],
                    "global_links": [],
                    "global_images": [],
                    "global_code_blocks": []
                }

                for file_path, file_data in parsed_files.items():
                    repo_ast["global_headings"].extend(file_data.get("headings", []))
                    repo_ast["global_tables"].extend(file_data.get("tables", []))
                    repo_ast["global_links"].extend(file_data.get("links", []))
                    repo_ast["global_images"].extend(file_data.get("images", []))
                    repo_ast["global_code_blocks"].extend(file_data.get("code_blocks", []))

                section_code_index = []

                for file_path, parsed in parsed_files.items():

                    for section in parsed.get("headings", []):

                        section_name = section["title"]
                        section_level = section.get("level", 1)
                        section_line = section.get("line", 0)

                        binding = CodeArchitectureAnalyzer.find_relevant_code(
                            section_name,
                            repo_ast,
                            {
                                "semantic_graph": code_graph,
                                "call_graph": call_graph,
                                "code_map": code_map
                            }
                        )

                        clean_binding = json.loads(json.dumps(binding, default=str))
                        section["code_scope"] = clean_binding
                        section["binding"] = clean_binding

                        section_code_index.append({
                            "section": section_name,
                            "file": file_path,
                            "level": section_level,
                            "line": section_line,
                            "binding": binding,
                            "parent": None,
                            "depth": section_level
                        })

                code_section_index = {}

                for entry in section_code_index:
                    binding = entry["binding"]

                    # parent NON lo calcoli qui, lo prendi dal parser
                    entry["parent"] = None  # default
                    
                    for func in binding.get("functions", []):
                        code_section_index.setdefault(func, []).append(entry["section"])

                    for clss in binding.get("classes", []):
                        code_section_index.setdefault(clss, []).append(entry["section"])

                # -------------------------------------------------
                # 2. AGGREGAZIONE STRUTTURALE (IMPORTANTE)
                # -------------------------------------------------
                repo_ast["section_code_index"] = section_code_index
                repo_ast["code_section_index"] = code_section_index

                # -------------------------------------------------
                # 3. LLM SOLO PER STRUTTURA (NON PARSING)
                # -------------------------------------------------
                prompt = f"""
                You are an expert in documentation architecture.

                You are given a FULL MARKDOWN AST.

                TASK:
                - detect documentation patterns
                - infer structure hierarchy
                - identify missing sections
                - propose ideal template structure

                DO NOT parse markdown.

                Return ONLY JSON:

                {{
                    "repo": "{owner}/{repo}",
                    "structure_summary": {{
                        "has_readme": true,
                        "has_api_docs": true,
                        "has_examples": true,
                        "depth_analysis": "low|medium|high",
                        "documentation_quality": "low|medium|high"
                    }},
                    "patterns": [],
                    "insights": []
                }}

                INPUT AST:
                {json.dumps(repo_ast, indent=2)}
                """

                result = llm_run(prompt, max_tokens=10000)
                analysis_json = extract_json(result)

                if analysis_json:
                    repo_structures[f"{owner}/{repo}"] = {
                        "ast": repo_ast,
                        "analysis": analysis_json
                    }

                    logger.info(f"[{self.name}] Parsed OK: {owner}/{repo}")

                else:
                    logger.warning(f"[{self.name}] Invalid JSON: {owner}/{repo}")

            except Exception as e:
                logger.warning(f"[{self.name}] Repo failed {owner}/{repo}: {e}")

        # -------------------------------------------------
        # 8. Prompt finale
        # -------------------------------------------------
        logger.info(f"\n[{self.name}] Building FINAL template...\n")

        prompt_template = """
            You are a Principal Software Documentation Architect.

            Your task is NOT to write documentation.

            Your task is to DESIGN the COMPLETE DOCUMENTATION STRUCTURE
            for a NEW software project.

            The final output must be a JSON document compatible with md-template.json.

            =========================================================
            IMPORTANT CONCEPT
            =========================================================

            The analyzed repositories are NOT templates to copy.

            The analyzed repositories represent:

            - documentation patterns
            - documentation strategies
            - documentation organization styles
            - file grouping approaches
            - section hierarchies
            - documentation best practices

            You MUST learn from them.

            You MUST NOT reproduce them.

            You MUST create a NEW documentation architecture specifically
            tailored to the software being analyzed.

            =========================================================
            INPUT SOURCES
            =========================================================

            1) Base Documentation Template
            (reference only)

            {base_template}

            ---------------------------------------------------------

            2) Documentation Structures Extracted From Real Repositories

            {repo_structures}

            ---------------------------------------------------------

            3) High Level Project Context

            {project_context}

            ---------------------------------------------------------

            4) Project Analysis Produced By Specialized Agents

            Project Tree:
            {project_tree}

            Languages:
            {language_info}

            Build System:
            {build_info}

            Usage Analysis:
            {usage_info}

            Code Architecture:
            {code_info}

            Documentation Targets:
            {doc_targets}

            Quality Analysis:
            {quality_info}

            =========================================================
            PRIMARY OBJECTIVE
            =========================================================

            Design the BEST possible markdown documentation architecture
            for THIS specific project.

            The structure must fit:

            - actual modules
            - actual services
            - actual APIs
            - actual workflows
            - actual deployment model
            - actual architecture
            - actual dependencies
            - actual security model
            - actual user flows

            discovered by the analyzers.

            =========================================================
            REASONING PROCESS
            =========================================================

            STEP 1

            Analyze all repository documentation structures.

            Identify:

            - recurring files
            - recurring sections
            - recurring subsection hierarchies
            - recurring documentation domains
            - recurring navigation models

            ---------------------------------------------------------

            STEP 2

            Analyze the target software.

            Determine:

            - software type
            - architectural complexity
            - deployment complexity
            - API complexity
            - module count
            - service count
            - integration count
            - security complexity
            - operational complexity

            ---------------------------------------------------------

            STEP 3

            Compare repository patterns with project needs.

            For each documentation area decide:

            - KEEP
            - MODIFY
            - REMOVE
            - CREATE NEW

            based on the actual project.

            ---------------------------------------------------------

            STEP 4

            Generate a NEW documentation architecture.

            The final structure must be:

            - project specific
            - analyzer driven
            - repository inspired
            - non copied
            - complete

            =========================================================
            FILE GENERATION RULES
            =========================================================

            For EACH markdown file define:

            - file path
            - purpose
            - sections
            - subsections
            - documentation targets

            Each section must belong to exactly one file.

            Avoid duplication.

            =========================================================
            SECTION GENERATION RULES
            =========================================================

            Sections must be generated from:

            - architecture analysis
            - APIs
            - modules
            - services
            - workflows
            - dependencies
            - deployment
            - security
            - configuration
            - testing
            - usage

            Only include sections that make sense for THIS project.

            Do not blindly reproduce repository structures.

            =========================================================
            DIRECTORY TREE RULES
            =========================================================

            The markdown_directory_tree must represent:

            - actual documentation hierarchy
            - actual navigation hierarchy
            - actual logical grouping

            It may differ from md-template.json if the project
            requires a better structure.

            =========================================================
            OUTPUT FORMAT
            =========================================================

            Return ONLY VALID JSON.

            Schema:

            {
            "documentation_strategy": {
                "documentation_type": "",
                "complexity": "",
                "rationale": ""
            },

            "markdown_directory_tree": {},

            "markdown_files": [
                {
                "path": "",
                "purpose": "",
                "derived_from": [],
                "project_entities": [],
                "sections": [
                    {
                    "title": "",
                    "purpose": "",
                    "source_reasoning": "",
                    "subsections": []
                    }
                ]
                }
            ],

            "coverage_map": {},

            "missing_docs_detected": [],

            "documentation_principles": [],

            "insights": [],

            "doc_targets_used": []
            }

            =========================================================
            CRITICAL RULES
            =========================================================

            DO NOT:

            - copy repository structures
            - copy repository file names blindly
            - copy repository sections blindly
            - replicate md-template.json as-is

            INSTEAD:

            - reason across ALL repositories
            - reason across ALL analyzers
            - reason across ALL project metadata
            - build a NEW documentation architecture

            The final architecture must look as if it had been
            designed manually by a senior documentation architect
            after studying both:

            1) similar projects
            2) the actual target project

            Return ONLY JSON.
            You MUST reply ONLY with a valid JSON object.
            Do not include any markdown, explanations, or introductory text.
            If you fail to return a pure JSON string, the system will break.

            """


        prompt_final = prompt_template.format(
            base_template=json.dumps(self.base_template, indent=2, ensure_ascii=False),
            repo_structures=json.dumps(repo_structures, indent=2, ensure_ascii=False),
            project_tree=json.dumps(project_tree, indent=2, ensure_ascii=False),
            language_info=json.dumps(language_info, indent=2, ensure_ascii=False),
            build_info=json.dumps(build_info, indent=2, ensure_ascii=False),
            usage_info=json.dumps(usage_info, indent=2, ensure_ascii=False),
            code_info=json.dumps(code_info, indent=2, ensure_ascii=False),
            doc_targets=json.dumps(doc_targets, indent=2, ensure_ascii=False),
            quality_info=json.dumps(quality_info, indent=2, ensure_ascii=False),
            project_context=json.dumps(project_context, indent=2, ensure_ascii=False),

            output_schema=json.dumps({
                "markdown_directory_tree": {},
                "markdown_files": [],
                "documentation_principles": [],
                "insights": [],
                "missing_docs_detected": [],
                "coverage_map": {},
                "doc_targets_used": []
            })
        )

        result_final = llm_run(prompt_final, max_tokens=10000)
        logger.info(f"\n[{self.name}] Result: {result_final}\n")
        final_structure = extract_json(result_final)
        if not final_structure:
            final_structure = {
                "error": "invalid_json",
                "raw": result_final
            }
        self.save_to_json(data=final_structure, raw_content=result_final)
        logger.info(f"[{self.name}] result: {parsed}")
        logger.info(f"[{self.name}] end running")
        return final_structure

