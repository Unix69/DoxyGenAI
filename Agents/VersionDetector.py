from crewai import Agent, Task
import os

class VersionDetector(Agent):
    def setup(self):
        self.role = "Rilevamento Versioni"
        self.goal = "Analizza VERSION.md e informazioni di rilascio"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        version_file = os.path.join(src_path, "VERSION.md")
        current_version = None
        previous_versions = []

        if os.path.exists(version_file):
            with open(version_file) as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines:
                    current_version = lines[0]
                    previous_versions = lines[1:]

        return {
            "current_version": current_version,
            "previous_versions": previous_versions
        }