from crewai import Agent, Task
import os
import re

class APIExtractor(Agent):
    def setup(self):
        self.role = "Estrazione API"
        self.goal = "Individua le API e le namespaces principali dal codice"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        apis = set()
        namespaces = set()

        for root, _, files in os.walk(src_path):
            for f in files:
                if f.endswith((".h", ".c", ".cpp")):
                    path = os.path.join(root, f)
                    with open(path, errors="ignore") as file:
                        content = file.read()
                        # pattern semplice: funzioni pubbliche come API
                        apis.update(re.findall(r"\b[A-Za-z_]\w*\s*\(.*?\)", content))
                        # pattern namespaces C++ o commenti speciali
                        namespaces.update(re.findall(r"\bnamespace\s+(\w+)", content))
        
        return {
            "apis": list(apis),
            "namespaces": list(namespaces)
        }
