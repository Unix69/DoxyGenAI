
import base64
import json
import os
import re


def extract_json(text: str):
    """
    Robust JSON extractor for LLM responses.
    Supports:
    - markdown fences
    - text before/after JSON
    - arrays or dicts
    - trailing commas
    - malformed wrapping text
    """

    if not text:
        return None

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # normalize quotes occasionally broken
    text = text.replace("\u201c", '"').replace("\u201d", '"')

    # ---------------------------------------------------
    # TRY DIRECT FULL JSON
    # ---------------------------------------------------
    try:
        return json.loads(text)
    except:
        pass

    # ---------------------------------------------------
    # FIND FIRST JSON OBJECT / ARRAY
    # ---------------------------------------------------
    candidates = []

    stack = []
    start = None

    for i, ch in enumerate(text):

        if ch in "{[":
            if not stack:
                start = i
            stack.append(ch)

        elif ch in "}]":
            if stack:
                stack.pop()

                if not stack and start is not None:
                    candidates.append(text[start:i+1])
                    start = None

    # ---------------------------------------------------
    # TRY ALL CANDIDATES
    # ---------------------------------------------------
    for c in candidates:

        # remove trailing commas
        cleaned = re.sub(r",(\s*[}\]])", r"\1", c)

        try:
            return json.loads(cleaned)
        except:
            continue

    return None



# ----------------------------
# Lettura ricorsiva file
# ----------------------------
def read_project_files(base_path: str, max_chars_per_file: int = 1000) -> dict:
    project_files = {}
    for root, _, files in os.walk(base_path):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_path)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                    project_files[rel_path] = file.read(max_chars_per_file)
            except Exception as e:
                project_files[rel_path] = f"<ERRORE lettura: {e}>"
    return project_files

# ----------------------------
# Lettura examples strutturati
# ----------------------------
def read_examples(base_path: str, max_chars_per_file: int = 1000) -> dict:
    examples = {}

    for project_name in os.listdir(base_path):
        project_dir = os.path.join(base_path, project_name)
        if not os.path.isdir(project_dir):
            continue

        example_src = {}
        example_template = {}

        for root, _, files in os.walk(project_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, project_dir)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read(max_chars_per_file)

                        # Separiamo src e template
                        if rel_path.startswith("src"):
                            example_src[rel_path] = content
                        else:
                            example_template[rel_path] = content

                except Exception as e:
                    example_template[rel_path] = f"<ERRORE: {e}>"

        examples[project_name] = {
            "src": example_src,
            "template": example_template
        }

    return examples

# ----------------------------
# Scrittura template adattato su disco
# ----------------------------
def save_template_to_disk(template_dict: dict, out_dir: str):
    if os.path.exists(out_dir):
        # opzionale: pulizia
        import shutil
        shutil.rmtree(out_dir)

    os.makedirs(out_dir, exist_ok=True)

    for path, content in template_dict.items():
        full_path = os.path.join(out_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            logger.error(f"[ERROR write] {full_path}: {e}")


def generate_doxygen_base(project_root: str, out_dir: str):
    """
    Genera:
    - Doxyfile base
    - header.html
    - footer.html
    - stylesheet.css
    usando Doxygen reale.
    """

    import subprocess
    import os

    os.makedirs(out_dir, exist_ok=True)

    # 1 genera Doxyfile
    subprocess.run(
        ["doxygen", "-g", os.path.join(out_dir, "Doxyfile")],
        check=True
    )

    doxyfile = os.path.join(out_dir, "Doxyfile")

    # 2 abilita header/footer generation
    with open(doxyfile, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "GENERATE_HTML = YES",
        "GENERATE_HTML = YES\nHTML_HEADER = header.html\nHTML_FOOTER = footer.html\nHTML_STYLESHEET = stylesheet.css"
    )

    with open(doxyfile, "w", encoding="utf-8") as f:
        f.write(content)

    # 3 esegue doxygen per generare i template
    subprocess.run(
        ["doxygen", doxyfile],
        cwd=out_dir,
        check=True
    )

    generated = {}

    html_dir = os.path.join(out_dir, "html")

    for name in ["header.html", "footer.html", "stylesheet.css"]:
        path = os.path.join(html_dir, name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                generated[name] = f.read()

    return {
        "doxyfile_path": doxyfile,
        "assets": generated
    }


def prefilter_files(files_dict):
    candidates = {}

    for path, content in files_dict.items():
        lower = path.lower()

        # filtra file troppo grandi
        if len(content) > 200_000:
            continue

        # keyword leggere su path
        if any(k in lower for k in [
            "build", "make", "cmake", "gradle", "pom",
            "package", "docker", "config", "ci", "pipeline"
        ]):
            candidates[path] = content
            continue

        # estensioni tipiche config
        if lower.endswith((".json", ".yml", ".yaml", ".xml", ".toml")):
            candidates[path] = content

    return candidates




def extract_build_candidates(files_dict, classification):
    candidates = {}

    for f in classification.get("files", []):
        if f.get("type") in [
            "build", "dependency", "config", "ci_cd", "container"
        ] and f.get("confidence", 0) > 0.5:

            path = f["path"]

            if path in files_dict:
                candidates[path] = files_dict[path][:3000]  # truncate sicurezza

    return candidates






def take_first_lines(files_dict, max_lines=50):
    sampled = {}

    for path, content in files_dict.items():
        try:
            # sicurezza: evita roba non stringa
            if not isinstance(content, str):
                continue

            lines = content.splitlines()

            # prendi solo le prime N righe
            first_lines = "\n".join(lines[:max_lines])

            sampled[path] = first_lines

        except Exception:
            continue

    return sampled


def extract_build_files(files_dict):
    BUILD_KEYWORDS = [
        "makefile",
        "cmakelists.txt",
        "meson.build",
        "build.gradle",
        "pom.xml",
        "package.json",
        "yarn.lock",
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "dockerfile",
        "docker-compose",
        ".github/workflows",
        ".gitlab-ci",
        "jenkinsfile",
        "helm",
        "k8s",
        "chart.yaml"
    ]

    filtered = {}

    for path, content in files_dict.items():
        lower_path = path.lower()

        if any(k in lower_path for k in BUILD_KEYWORDS):
            filtered[path] = content

    return filtered


def to_b64(data: dict) -> str:
    raw = json.dumps(data)
    return base64.b64encode(raw.encode()).decode()





class Tools:
    pass