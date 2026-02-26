from crewai import Agent, Task
import os
import re

class FeatureDetector(Agent):
    def setup(self):
        self.role = "Rilevamento Features"
        self.goal = "Individua le funzionalità principali implementate nel progetto"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        features = set()

        for root, _, files in os.walk(src_path):
            for f in files:
                if f.endswith((".c", ".cpp", ".py")):
                    path = os.path.join(root, f)
                    with open(path, errors="ignore") as file:
                        content = file.read()
                        # pattern semplice: funzioni chiave come feature
                        features.update(re.findall(r"\b(create|delete|update|generate|read|login|logout)\w*\b", content, re.IGNORECASE))

        return {"features": list(features)}
