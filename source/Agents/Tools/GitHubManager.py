import base64
import hashlib
import os
import json
import re
from typing import Any, Dict, List

from dotenv import load_dotenv
import requests

from Agents.Agent import Agent
from Agents.Logger import logger
from Agents.Tools.Tools import extract_json
from Agents.Tools.LLM import llm_run

 
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")



class MarkdownElementExtractor:

    def __init__(self):
        self.heading_re = re.compile(r'^\s*(#{1,6})\s+(.+)$')
        self.image_re = re.compile(r'!\[(.*?)\]\((.*?)\)')
        self.link_re = re.compile(r'\[(.*?)\]\((.*?)\)')
        self.code_block_re = re.compile(r'```(\w+)?\s*\n([\s\S]*?)```', re.DOTALL)
        self.table_re = re.compile(r'(\|.*\|(\n\|.*\|)+)', re.MULTILINE)

    def build_heading_tree(self, headings):

        root = []
        stack = []

        headings = sorted(headings, key=lambda x: x.get("line", 0))

        for h in headings:
            node = {
                "id": h["id"],
                "level": h["level"],
                "title": h["title"],
                "line": h["line"],
                "end_line": h["end_line"],
                "children": [],
                "file_path": h["file_path"],
                "parent_id": None
            }

            while stack and stack[-1]["level"] >= node["level"]:
                stack.pop()

            if not stack:
                root.append(node)
            else:
                node["parent_id"] = stack[-1].get("id")
                stack[-1]["children"].append(node)

            stack.append(node)

        return root


    def _parse_table(self, rows):

        clean = []

        for r in rows:
            if set(r.replace("|", "").replace(":", "").strip()) <= {"-"}:
                continue

            cells = [c.strip() for c in r.split("|") if c.strip()]
            if cells:
                clean.append(cells)

        if not clean:
            return None

        return {
            "header": clean[0],
            "rows": clean[1:]
        }

    def parse(self, markdown: str, file_path: str) -> Dict[str, Any]:

        lines = markdown.split("\n")
        headings = self.extract_headings(lines, file_path)
        tree = self.build_heading_tree(headings)

        return {
            "headings": headings,
            "heading_tree": tree,
            "images": self.extract_images(markdown),
            "links": self.extract_links(markdown),
            "code_blocks": self.extract_code_blocks(markdown),
            "tables": self.extract_tables(markdown),
            "sections": self.build_sections_from_tree(tree, lines),
            "raw_text": markdown
        }



    def make_id(self, file_path: str, line: int, title: str) -> str:
        raw = f"{file_path.strip().lower()}|{line}|{title.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    # -------------------------------------------------
    # HEADINGS (H1-H6)
    # -------------------------------------------------
    def extract_headings(self, lines, file_path: str):

        headings = []

        for i, line in enumerate(lines):
            match = self.heading_re.match(line.strip())

            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                
                headings.append({
                    "id": self.make_id(file_path, i, text),
                    "level": level,
                    "title": text,
                    "line": i,
                    "end_line": None,
                    "file_path": file_path
                })

        
        for i in range(len(headings)):
            start = headings[i]["line"]

            end = len(lines)

            for j in range(i + 1, len(headings)):
                if headings[j]["level"] <= headings[i]["level"]:
                    end = headings[j]["line"]
                    break

            headings[i]["end_line"] = end

        return headings

    # -------------------------------------------------
    # IMAGES
    # -------------------------------------------------
    def extract_images(self, markdown: str) -> List[Dict]:
        return [
            {
                "alt": match.group(1),
                "path": match.group(2)
            }
            for match in self.image_re.finditer(markdown)
        ]

    # -------------------------------------------------
    # LINKS
    # -------------------------------------------------
    def extract_links(self, markdown: str) -> List[Dict]:
        return [
            {
                "text": match.group(1),
                "url": match.group(2)
            }
            for match in self.link_re.finditer(markdown)
        ]

    # -------------------------------------------------
    # CODE BLOCKS
    # -------------------------------------------------
    def extract_code_blocks(self, markdown: str) -> List[Dict]:
        blocks = []

        for match in self.code_block_re.finditer(markdown):
            language = match.group(1) or "unknown"
            code = match.group(2)

            blocks.append({
                "language": language,
                "code": code.strip()
            })

        return blocks

    def build_sections_from_tree(self, tree, lines):

        sections = []
        visited = set()

        def walk(node):

            if node["id"] in visited:
                return
            visited.add(node["id"])

            start = node["line"]
            end = node.get("end_line", len(lines))

            sections.append({
                "id": node["id"],
                "name": node["title"],
                "level": node["level"],
                "file_path": node.get("file_path"),
                "parent_id": node.get("parent_id"),
                "content": "\n".join(lines[start:end])
            })

            for child in node.get("children", []):
                walk(child)

        for root in tree:
            walk(root)

        return sections

    # -------------------------------------------------
    # TABLES (basic markdown table detection)
    # -------------------------------------------------
    def extract_tables(self, markdown: str):

        lines = markdown.split("\n")
        tables = []
        current = []

        for line in lines:
            if "|" in line and line.count("|") >= 2:
                current.append(line)
            else:
                if len(current) > 1:
                    table = self._parse_table(current)
                    if table:
                        tables.append(table)
                current = []

        if len(current) > 1:
            table = self._parse_table(current)
            if table:
                tables.append(table)

        return tables
    

    
class GitHubManager:
    def __init__(self, github_token: str, username: str = None):
        self.github_token = github_token
        self.username = username
        self.headers = {"Authorization": f"token {self.github_token}"}

    # ----------------------------
    # Helper: recupera info README + badge CI
    # ----------------------------
    def _get_readme_info(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            return {"readme_length": 0, "ci_badges": []}
        data = r.json()
        content = base64.b64decode(data.get("content", "")).decode(errors="ignore")
        readme_length = len(content)

        # Cerca badge CI (Travis, GitHub Actions, CircleCI, Jenkins)
        ci_badges = re.findall(
            r"!\[.*?\]\(.*?(travis-ci\.org|github\.com/.*/.*/actions|circleci\.com|jenkins\.io).*?\)",
            content,
            re.IGNORECASE
        )
        return {"readme_length": readme_length, "ci_badges": ci_badges}

    # ----------------------------
    # Recupera repo utente con paginazione
    # ----------------------------
    def get_user_repos(self, max_repos=1):
        if not self.username:
            return []

        repos = []
        page = 1
        per_page = min(max_repos, 100)

        while len(repos) < max_repos:
            url = f"https://api.github.com/users/{self.username}/repos"
            params = {"sort": "updated", "per_page": per_page, "page": page}
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                break
            data = r.json()
            if not data:
                break

            for repo in data:
                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue
                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])
                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "watchers": repo["watchers_count"],
                    "language": repo.get("language"),
                    "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "fork": repo["fork"],
                    "archived": repo["archived"],
                    "is_template": repo.get("is_template", False),
                    **readme_info
                })
                if len(repos) >= max_repos:
                    break
            page += 1

        return repos

    # ----------------------------
    # Recupera repo globali popolari con paginazione
    # ----------------------------
    def get_global_repos(self, min_stars=5000, max_repos=1):
        repos = []
        page = 1
        per_page = min(max_repos, 100)

        while len(repos) < max_repos:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"stars:>{min_stars}",
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
                "page": page
            }
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                break
            data = r.json()
            if not data.get("items"):
                break

            for repo in data["items"]:
                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue
                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])
                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "watchers": repo["watchers_count"],
                    "language": repo.get("language"),
                    "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "fork": repo["fork"],
                    "archived": repo["archived"],
                    "is_template": repo.get("is_template", False),
                    **readme_info
                })
                if len(repos) >= max_repos:
                    break
            page += 1

        return repos

    # ----------------------------
    # Merge intelligente delle repo
    # ----------------------------
    @staticmethod
    def merge_repos(*repo_lists, max_total=10):
        seen = set()
        merged = []

        for repo_list in repo_lists:
            for repo in repo_list:
                key = (repo["owner"], repo["repo"])
                if key not in seen:
                    seen.add(key)
                    merged.append(repo)
                if len(merged) >= max_total:
                    return merged
        return merged

    # ----------------------------
    # Scopre repo rilevanti dal contesto
    # ----------------------------
    def discover_repos_from_context(self, crew_context: dict, max_repos=1):
        lang = crew_context.get("LanguageDetector", {}).get("primary_language", "")
        build = crew_context.get("BuildSystemDetector", {}).get("build_systems", [])

        base_queries = []

        # ------------------------
        # QUERY 1: linguaggio + stars
        # ------------------------
        if lang:
            base_queries.append(f"language:{lang}")

        base_queries.append("stars:>1000")

        # ------------------------
        # QUERY 2: API / framework hint
        # ------------------------
        if lang:
            base_queries.append(f"language:{lang} topic:api")
            base_queries.append(f"language:{lang} topic:web")

        # ------------------------
        # QUERY 3: build system SOLO se utile
        # ------------------------
        if build:
            b = build[0].lower()
            if b in ["pip", "poetry", "pipenv", "setuptools"]:
                base_queries.append(f"language:{lang} topic:python")

        # ------------------------
        # QUERY 4: documentation (più soft)
        # ------------------------
        base_queries.append("in:readme documentation")
        base_queries.append("topic:documentation")

        repos = []
        seen = set()

        for query in base_queries:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": max_repos
            }

            r = requests.get(url, headers=self.headers, params=params)

            if r.status_code != 200:
                continue

            items = r.json().get("items", [])

            for repo in items:
                key = (repo["owner"]["login"], repo["name"])

                if key in seen:
                    continue

                if repo["fork"] or repo["archived"] or repo.get("is_template", False):
                    continue

                seen.add(key)

                readme_info = self._get_readme_info(repo["owner"]["login"], repo["name"])

                repos.append({
                    "owner": repo["owner"]["login"],
                    "repo": repo["name"],
                    "stars": repo["stargazers_count"],
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                    "language": repo.get("language"),
                    **readme_info
                })

                if len(repos) >= max_repos:
                    return repos

        return repos

    # ----------------------------
    # Merge intelligente delle repo
    # ----------------------------
    @staticmethod
    def merge_repos(*repo_lists, max_total=6):
        seen = set()
        merged = []

        for repo_list in repo_lists:
            for repo in repo_list:
                key = (repo["owner"], repo["repo"])
                if key not in seen:
                    seen.add(key)
                    merged.append(repo)
                if len(merged) >= max_total:
                    return merged
        return merged


    def fetch_repo_md_files(
        self,
        owner: str,
        repo: str,
        branch: str = None,
        max_files: int = 30,
        max_chars_per_file: int = 12000
    ) -> dict:
        """
        Scarica tutti i file markdown del repository.

        Return:
        {
            "README.md": "...",
            "docs/install.md": "...",
            ...
        }

        Features:
        - prova branch automatico main/master/default_branch
        - recursive tree scan
        - solo file .md/.markdown/.mdx
        - limita numero file
        - limita dimensione contenuto
        """

        logger.info(f"[GitHubManager] Fetch markdown files: {owner}/{repo}")

        md_files = {}

        # -----------------------------------
        # STEP 1 - Recupera metadata repo
        # -----------------------------------
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        r = requests.get(repo_url, headers=self.headers, timeout=20)

        if r.status_code != 200:
            logger.warning(
                f"[GitHubManager] Cannot read repo metadata {owner}/{repo} "
                f"status={r.status_code}"
            )
            return {}

        repo_info = r.json()

        default_branch = repo_info.get("default_branch", "main")

        if not branch:
            branch = default_branch

        # -----------------------------------
        # STEP 2 - Tree ricorsivo
        # -----------------------------------
        tree_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/git/trees/{branch}?recursive=1"
        )

        r = requests.get(tree_url, headers=self.headers, timeout=30)

        if r.status_code != 200:
            logger.warning(
                f"[GitHubManager] Tree fetch failed {owner}/{repo} "
                f"branch={branch} status={r.status_code}"
            )
            return {}

        data = r.json()
        tree = data.get("tree", [])

        logger.info(
            f"[GitHubManager] {owner}/{repo} tree objects: {len(tree)}"
        )

        # -----------------------------------
        # STEP 3 - Filtra markdown files
        # -----------------------------------
        markdown_paths = []

        for item in tree:
            if item.get("type") != "blob":
                continue

            path = item.get("path", "")
            lower = path.lower()

            if lower.endswith((".md", ".markdown", ".mdx")):
                markdown_paths.append(path)

        markdown_paths = markdown_paths[:max_files]

        logger.info(
            f"[GitHubManager] {owner}/{repo} markdown files found: "
            f"{len(markdown_paths)}"
        )

        # -----------------------------------
        # STEP 4 - Scarica contenuti raw
        # -----------------------------------
        for path in markdown_paths:

            raw_url = (
                f"https://raw.githubusercontent.com/"
                f"{owner}/{repo}/{branch}/{path}"
            )

            try:
                rr = requests.get(raw_url, headers=self.headers, timeout=20)

                if rr.status_code == 200:
                    text = rr.text[:max_chars_per_file]
                    md_files[path] = text

                    logger.info(
                        f"[GitHubManager] OK {owner}/{repo}/{path} "
                        f"({len(text)} chars)"
                    )

                else:
                    logger.warning(
                        f"[GitHubManager] RAW fail {path} "
                        f"status={rr.status_code}"
                    )

            except Exception as e:
                logger.warning(
                    f"[GitHubManager] Error downloading {path}: {e}"
                )

        logger.info(
            f"[GitHubManager] Completed {owner}/{repo}: "
            f"{len(md_files)} markdown files"
        )

        return md_files
