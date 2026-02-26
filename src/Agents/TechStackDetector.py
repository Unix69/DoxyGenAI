from crewai import Agent, Task

class TechStackDetector(Agent):
    def setup(self):
        self.role : str =  "Rilevamento Tech Stack e toolchain"
        self.goal : str =  (
            "Analizza i file di configurazione e build del template "
            "e del nuovo progetto per identificare linguaggi, librerie, "
            "framework e tool necessari (es. Doxygen, Make, Graphviz)."
        )

    async def run(self, task: Task):
        import os

        src_path = task.input.get("src_path", "./src")
        template_files = task.input.get("template_files", [])

        tech_stack = set()
        versions = {}

        # Controllo tool comuni e build scripts
        for f in template_files + os.listdir(src_path):
            if f.endswith(".py"):
                tech_stack.add("Python")
            if f.endswith(".c") or f.endswith(".h"):
                tech_stack.add("C")
            if f in ["Makefile"]:
                tech_stack.add("GNU Make")
            if f in ["Doxyfile", "doxygen.sh", "doxygen.ini"]:
                tech_stack.add("Doxygen")
            if f.endswith(".html") or f.endswith(".css"):
                tech_stack.add("Web")
            if f.endswith(".sh"):
                tech_stack.add("Bash")

        if "Doxygen" in tech_stack:
            versions["Doxygen"] = "1.9.7"
        if "Graphviz" in tech_stack:
            versions["Graphviz"] = "3.1.0"

        return {
            "tech_stack": list(tech_stack),
            "versions": versions
        }