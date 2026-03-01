from crewai import Agent, Task
import os

class ReleasePolicyDetector(Agent):
    def setup(self):
        self.role = "Analisi Release Policy"
        self.goal = "Estrae la policy di rilascio da RELEASE_POLICY.md"

    async def run(self, task: Task):
        src_path = task.input["new_src_path"]
        file_path = os.path.join(src_path, "RELEASE_POLICY.md")
        release_rules = ""
        cadence = ""
        notes = ""

        if os.path.exists(file_path):
            with open(file_path) as f:
                content = f.read()
                release_rules = content[:500]  # esempio semplificato
                # TODO: usare NLP per estrarre cadence e policy
        return {
            "release_rules": release_rules,
            "cadence": cadence,
            "policy_notes": notes
        }