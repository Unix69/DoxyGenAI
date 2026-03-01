from crewai import Agent, Task
import json

class Planner(Agent):
    def setup(self):
        self.role = "Pianificazione adattamento template"
        self.goal = (
            "Prende l'analisi dei detector agent e produce un piano per trasformare "
            "il template puro in un template specifico per il nuovo progetto. "
            "Considera gli esempi di trasformazioni precedenti per apprendere le regole."
        )

    async def run(self, task: Task):
        
        detectors = task.input
        examples_index = task.input.get("examples_index", [])

        plan = {
            "directory_tree": {
                ".github": True,
                "Images": True,
                "Usage": True,
                "Version": True,
                "docs": True,
                "src": "copy_new_source",
            },
            "files_to_generate": [],
            "update_md": {},
            "update_html": {},
            "update_scripts": {},
            "deploy": True
        }

        # ======= Pianificazione MD files =======
        md_templates = [
            "README.md", "API.md", "FEATURE.md", "BUG.md", "FIX.md",
            "CHANGELOG.md", "NAMESPACE.md", "RELEASE_POLICY.md",
            "VERSION.md", "ACTORS.md", "ROLES.md", "USECASES.md",
            "ADMINISTRATOR_GUIDE.md", "USER_GUIDE.md", "DEVELOPMENT_GUIDE.md",
            "PROJECT.md", "CONTACT_US.md", "CODE_OF_CONDUCT.md"
        ]

        for md in md_templates:
            plan["update_md"][md] = {
                "update_from_template": True,
                "update_from_examples": examples_index,  # riferimenti ai tuoi esempi
                "replace_sections": True  # flag generico che il Transformer userà
            }

        plan["update_html"] = {
            "index.html": {"template": True},
            "header.html": {"template": True},
            "footer.html": {"template": True},
            "index.css": {"template": True},
            "directory-tree.js": {"template": True},
            "link.js": {"template": True}
        }

        plan["update_scripts"] = {
            "Makefile": {"template": True, "update_for_new_src": True},
            "doxygen.sh": {"template": True},
            "doxygen.ini": {"template": True},
            "Doxyfile": {"template": True, "update_paths": True}
        }

        plan["deploy"] = {
            "generate_docs": True,
            "use_makefile_target": "doc"
        }

        return plan