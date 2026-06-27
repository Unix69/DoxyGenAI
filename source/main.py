from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import json
from dotenv import load_dotenv


import Agents

from Agents.Tools.Tools import read_project_files

from Agents.Crew import Crew

from Agents.Logger import logger
from Agents.ProjectTreeAnalyzer import ProjectTreeAnalyzer
from Agents.LanguageDetector import LanguageDetector
from Agents.DependencyDetector import DependencyDetector
from Agents.BuildSystemDetector import BuildSystemDetector
from Agents.CodeArchitectureAnalyzer import CodeArchitectureAnalyzer
from Agents.APIAnalyzer import APIAnalyzer
from Agents.SecurityPermissionAnalyzer import SecurityPermissionAnalyzer
from Agents.UsageAnalyzer import UsageAnalyzer
from Agents.DocumentationAnalyzer import DocumentationAnalyzer
from Agents.DevOpsAnalyzer import DevOpsAnalyzer
from Agents.VersioningAnalyzer import VersioningAnalyzer
from Agents.QualityAnalyzer import QualityAnalyzer
from Agents.ProjectMetadataAnalyzer import ProjectMetadataAnalyzer
from Agents.MDTemplateAnalyzer import MDTemplateAnalyzer

 
dotenv_path = os.path.join(os.path.dirname(__file__), 'Agents', '.env')

# Carica il file specificando il path
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logger.info(f".env charged correctly: {dotenv_path}")
else:
    logger.critical(f".env non found: {dotenv_path}")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
SRC_PATH=os.getenv("SRC_PATH")
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(project_root, SRC_PATH)



def load_project_context(path="./project_context.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)




def process_project(project_path, task):
    # Pass project_path into the task so the agent knows what to analyze
    current_task = task.copy()
    current_task["project_root"] = project_path
    
    project_name = os.path.basename(project_path)
    crew = Crew()
    crew.add_agent(ProjectTreeAnalyzer())
    crew.add_agent(LanguageDetector())
    crew.add_agent(DependencyDetector())
    crew.add_agent(BuildSystemDetector())
    crew.add_agent(CodeArchitectureAnalyzer())
    crew.add_agent(APIAnalyzer())
    crew.add_agent(SecurityPermissionAnalyzer())
    crew.add_agent(UsageAnalyzer())
    crew.add_agent(DocumentationAnalyzer())
    crew.add_agent(DevOpsAnalyzer())
    crew.add_agent(VersioningAnalyzer())
    crew.add_agent(QualityAnalyzer())
    crew.add_agent(ProjectMetadataAnalyzer())
    crew.add_agent(MDTemplateAnalyzer())
    #crew.add_agent(MDDocumentationMaker())
    #crew.add_agent(DoxygenConfigBuilder())
    #crew.add_agent(DoxygenDocumentationUXBuilder())
    #crew.add_agent(DeploymentStrategyResolver())
    #crew.add_agent(DocumentationDeploymentGenerator())
    
    # Return both the name and the results
    result_data = crew.run(current_task)
    return {"name": project_name, "data": result_data}





# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    logger.info("\n=== Start DOXYGEN AI CREW ===\n")

    # ----------------------------
    # Lettura nuovo progetto
    # ----------------------------
    src_files = read_project_files(SRC_PATH)
    project_context = load_project_context()
    
    task = {
        "project_context": project_context,
        "repos": [
                {"owner": "pallets", "repo": "flask"},
                {"owner": "fastapi", "repo": "fastapi"}
        ],
        "github_token": GITHUB_TOKEN,
        "github_username": GITHUB_USERNAME,
        "project_root": "./docs",          # cartella dove generare doc
        "files_dict": src_files,           # dizionario file sorgente
        "deployment_preferences": {
            "type": "static",
            "platform": "github_pages",
            "branch": "main",
            "docs_path": "docs",
            "custom_domain": None
        }
    }

    logger.info("\n=== Task ===\n")
    logger.info(str(task))



    projects = [os.path.join(SRC_PATH, d) for d in os.listdir(SRC_PATH) 
                if os.path.isdir(os.path.join(SRC_PATH, d))]
    
    func = partial(process_project, task=task)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # returns a list of dictionaries
        results = list(executor.map(func, projects))

    # Log results
    for res in results:
        logger.info(f"\n--- Results for {res['name']} ---")
        logger.info(json.dumps(res['data'], indent=2))

    # ----------------------------
    # Inizializzazione Crew
    # ----------------------------
    

    logger.info("\n=== CREW Results ===\n")

    for agent_name, output in results.items():
        logger.info(f"\n--- {agent_name} ---")

        if isinstance(output, dict):
            logger.info(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            logger.info(output)


    logger.info("\n=== End DOXYGEN AI CREW ===\n")
