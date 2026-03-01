from crewai import Agent, Task
import os
import re

class UseCaseDetector(Agent):
    def setup(self):
        self.role = "Identificazione usecases e actors"
        self.goal = "Individua gli attori principali e i casi d'uso dal codice"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        actors = set()
        usecases = set()

        for root, _, files in os.walk(src_path):
            for f in files:
                if f.endswith((".c", ".cpp", ".h", ".py")):
                    path = os.path.join(root, f)
                    with open(path, errors="ignore") as file:
                        content = file.read()
                        # pattern molto semplice: cerca nomi comuni di actors e funzioni
                        actors.update(re.findall(r"\b(Admin|User|Developer|Client|Server)\b", content))
                        usecases.update(re.findall(r"\b(login|logout|create|delete|update|generate|read)\w*\b", content, re.IGNORECASE))

        return {
            "actors": list(actors),
            "usecases": list(usecases)
        }



class RolesActorsUsecasesDetector(Agent):
    def setup(self):
        self.role = "Roles, Actors e Usecases"
        self.goal = "Analizza ACTORS.md, ROLES.md e USECASES.md"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        data = {}
        for md in ["ACTORS.md", "ROLES.md", "USECASES.md"]:
            path = os.path.join(src_path, md)
            if os.path.exists(path):
                with open(path) as f:
                    data[md.replace(".md","").lower()] = f.read().splitlines()
            else:
                data[md.replace(".md","").lower()] = []

        return data