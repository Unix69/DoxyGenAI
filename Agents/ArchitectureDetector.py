from crewai import Agent, Task
import os

class ArchitectureDetector(Agent):
    def setup(self):
        self.role = "Analisi architettura progetto"
        self.goal = (
            "Analizza la struttura del template e del nuovo progetto "
            "per identificare moduli, layer e pattern architetturali "
            "(monolitico, modulare, layered) e directory documentali."
        )

    async def run(self, task: Task):
        import os

        src_path = task.input.get("src_path", "./src")
        template_root = task.input.get("template_root", ".")

        modules = []
        layers = ["src"]  # src è sempre il layer principale

        # Analizza cartelle principali del template
        for folder in ["docs", "Usage", "Version", "Images"]:
            path = os.path.join(template_root, folder)
            if os.path.exists(path):
                layers.append(folder)

        # Moduli trovati in src
        if os.path.exists(src_path):
            for item in os.listdir(src_path):
                item_path = os.path.join(src_path, item)
                if os.path.isdir(item_path):
                    modules.append(item)
        
        # Pattern architetturale semplice
        if len(modules) > 1:
            architecture = "modulare + layered"
        else:
            architecture = "monolitico"

        return {
            "architecture": architecture,
            "modules": modules,
            "layers": layers
        }