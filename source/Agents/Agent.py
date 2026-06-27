
import os
import json
from typing import Dict, Any


from Agents.Logger import logger




# ----------------------------
# Base Agent
# ----------------------------
class Agent:
    def __init__(self, name: str, depends_on=None):
        self.name = name
        self.depends_on = depends_on or []
        self.lock = None

    def get_agent_output(self, crew_context: dict, agent_name: str) -> dict:
        # Usiamo il lock per una lettura sicura
        with self.lock:
            results = crew_context.get("results", {})
            return results.get(agent_name, {})

    def save_result(self, crew_context: dict, data: dict):
        # Usiamo il lock per una scrittura sicura
        with self.lock:
            if "results" not in crew_context:
                crew_context["results"] = {}
            crew_context["results"][self.name] = data

    def run(self, task: Dict[str, Any], crew_context: Dict[str, Any]) -> Any:
        raise NotImplementedError()
    
    def get_task(self, task, key, default=None):
        return task.get(key, default)

    def get_metadata(self, crew_context):
        return crew_context.get("metadata", {})

    def safe_get(self, data, key, default=None):
        if not isinstance(data, dict):
            return default
        return data.get(key, default)
    
    def save_to_json(self, data: Any, output_dir: str = "crew_outputs", raw_content: str = None):
        """
        Saves agent results to a JSON file named after the class.
        Logs status using standard logging levels.
        """
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                logger.info(f"Created output directory: {output_dir}")
            except Exception as e:
                logger.critical(f"Failed to create directory {output_dir}: {e}")
                return

        file_name = f"{self.__class__.__name__}.json"
        file_path = os.path.join(output_dir, file_name)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"[{self.name}] Successfully saved results to {file_path}")
            
            if raw_content:
                raw_path = f"{file_path}.raw.txt"
                with open(raw_path, 'w', encoding='utf-8') as f:
                    f.write(raw_content)
                logger.debug(f"[{self.name}] Raw output saved to {raw_path}")
                    
        except Exception as e:
            logger.error(f"[{self.name}] Failed to save results to {file_path}: {e}")

    
    def load_existing_result(self, output_dir: str = "crew_outputs"):
        """
        Controlla se esiste un file JSON valido per l'agente.
        Ritorna il dizionario se valido, altrimenti None.
        """
        file_path = os.path.join(output_dir, f"{self.__class__.__name__}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Verifica basica che non sia un errore salvato precedentemente
                if "error" not in data:
                    logger.info(f"[{self.name}] Found valid cached result. Skipping execution.")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"[{self.name}] Existing JSON is invalid or corrupted: {e}")
        
        return None