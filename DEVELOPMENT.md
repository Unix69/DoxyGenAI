# 🛠️ Development & Extension Guide

Learn how to safely modify, optimize, and inject custom analytical agents into the multi-agent DAG engine.

---

## 🧑‍💻 Implementing a Custom Agent

To expand the extraction capabilities of your framework, follow this clean template to inject a new custom agent.

### 1. Create your Agent File
Create a new script inside the <code>Agents/</code> package folder (e.g., <code>DatabaseSchemaAnalyzer.py</code>):

<pre><code>
import json
from Agents.Agent import Agent
from Agents.Logger import logger

class DatabaseSchemaAnalyzer(Agent):
    def __init__(self):
        # Define the agent name and any agents it depends on
        super().__init__("DatabaseSchemaAnalyzer", depends_on=["ProjectTreeAnalyzer"])

    def run(self, task, crew_context):
        logger.info(f"[{self.name}] starting data layer mapping...")
        
        # 1. Look for existing cached run outputs
        cached_result = self.load_existing_result()
        if cached_result:
            self.save_result(crew_context, cached_result)
            return cached_result

        # 2. Extract context loaded by parent dependencies
        tree_data = self.get_agent_output(crew_context, "ProjectTreeAnalyzer")
        
        # 3. Formulate analysis payload
        analyzed_schema = {
            "detected_databases": ["PostgreSQL"],
            "orm_layer": "SQLAlchemy",
            "confidence_score": 0.95
        }

        # 4. Save and return your structured results
        self.save_to_json(data=analyzed_schema)
        self.save_result(crew_context, analyzed_schema)
        return analyzed_schema
</code></pre>

### 2. Register the Agent in the Crew Pipeline
Modify your application initialization inside <code>main.py</code> to activate the custom behavior:

<pre><code>
from Agents.DatabaseSchemaAnalyzer import DatabaseSchemaAnalyzer

# Initialize Crew coordinator instance
crew = Crew(max_workers=8)

# Inject your custom analyzer alongside default modules
crew.add_agent(ProjectTreeAnalyzer())
crew.add_agent(DatabaseSchemaAnalyzer())

# Trigger concurrent pipeline process execution
results = crew.run(task)
</code></pre>

---

## ⚠️ Architectural Guardrails & Best Practices

When extending this framework, ensure you adhere to the following operational design rules:
1. **State Concurrency Rules**: Never directly modify variables inside <code>crew_context</code> without utilizing <code>self.lock</code>. Always leverage <code>self.save_result()</code> or <code>self.get_agent_output()</code> to interact safely with the shared execution state.
2. **Strict JSON Compliance**: Ensure your LLM parsing layers return strict JSON formats. Fall back to safety wrappers like <code>extract_json(result) or {"error": "invalid_json"}</code> to prevent unhandled runtime parsing crashes.
3. **Acyclic Dependency Tracking**: When adding items to <code>depends_on</code>, verify that you do not accidentally create a circular tracking path, which will immediately fail the <code>verify_dag()</code> pre-flight check.