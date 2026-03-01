from crewai import Agent, Task
import os
import shutil

class Transformer(Agent):
    def setup(self):
        self.role = "Trasformazione template avanzata"
        self.goal = (
            "Applica il piano generato dal PlannerAgent: "
            "aggiorna tutti i file MD/HTML/CSS/JS, aggiorna Makefile e Doxyfile, "
            "crea directory tree e copia sorgente nuovo progetto."
        )

    async def run(self, task: Task):
        plan = task.input.get("plan", {})
        new_src = task.input.get("src_path", "./src")
        template_root = task.input.get("template_root", "./EmbeddedDocsTemplates")
        output_root = task.input.get("output_root", "./project_out")

        os.makedirs(output_root, exist_ok=True)

        # ======= Creazione directory tree =======
        for folder, value in plan.get("directory_tree", {}).items():
            folder_path = os.path.join(output_root, folder)
            os.makedirs(folder_path, exist_ok=True)
            if value == "copy_new_source":
                src_dest = os.path.join(output_root, "src")
                shutil.copytree(new_src, src_dest, dirs_exist_ok=True)

        # ======= Copia e aggiornamento MD files =======
        for md_file, md_plan in plan.get("update_md", {}).items():
            src_md = os.path.join(template_root, md_file)
            dest_md = os.path.join(output_root, md_file)
            if os.path.exists(src_md):
                shutil.copy2(src_md, dest_md)
                # Qui si possono aggiungere funzioni di aggiornamento se replace_sections=True
                # es. usare LLM per riscrivere contenuti MD specifici per nuovo src

        # ======= Copia HTML/CSS/JS =======
        for html_file, html_plan in plan.get("update_html", {}).items():
            src_html = os.path.join(template_root, html_file)
            dest_html = os.path.join(output_root, html_file)
            if os.path.exists(src_html):
                shutil.copy2(src_html, dest_html)
                # eventuali modifiche automatiche via LLM

        # ======= Aggiornamento script =======
        for script_file, script_plan in plan.get("update_scripts", {}).items():
            src_script = os.path.join(template_root, script_file)
            dest_script = os.path.join(output_root, script_file)
            if os.path.exists(src_script):
                shutil.copy2(src_script, dest_script)
                # modifiche script: aggiorna percorsi, Makefile targets, Doxyfile paths ecc.

        return {"status": "done", "output_root": output_root}