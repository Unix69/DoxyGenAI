from crewai import Agent, Task
import os

class BugFixChangeDetector(Agent):
    def setup(self):
        self.role = "Analisi Bug, Fix e Changelog"
        self.goal = "Estrae informazioni da BUG.md, FIX.md e CHANGELOG.md"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        data = {}
        for md in ["BUG.md", "FIX.md", "CHANGELOG.md"]:
            path = os.path.join(src_path, md)
            if os.path.exists(path):
                with open(path) as f:
                    data[md.replace(".md","").lower()] = f.read().splitlines()
            else:
                data[md.replace(".md","").lower()] = []

        return data