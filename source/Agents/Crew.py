import os
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dotenv import load_dotenv
import time
import threading
import networkx as nx


from Agents.Agent import Agent
from Agents.Logger import logger


 
load_dotenv()




class Crew:

    def __init__(self, max_workers=8):
        self.agents = []
        self.max_workers = max_workers
        self.context_lock = threading.Lock()

    def add_agent(self, agent: Agent):
        agent.lock = self.context_lock
        self.agents.append(agent)

    def verify_dag(self):
        """Verifica che non ci siano cicli nelle dipendenze prima di partire."""
        dag = nx.DiGraph()
        for agent in self.agents:
            dag.add_node(agent.name)
            for dep in agent.depends_on:
                dag.add_edge(dep, agent.name)
        
        if not nx.is_directed_acyclic_graph(dag):
            cycle = nx.find_cycle(dag, orientation="original")
            raise Exception(f"Deadlock detected: dependency cycle {cycle}")
        logger.info("[Crew] DAG validated")

    def run(self, task: dict) -> dict:
        logger.info(f"[Crew] verify DAG")
        self.verify_dag()
        
        logger.info(f"[Crew] start running")
        
        crew_context = {"results": {}}
        completed_agents = set()
        failed_agents = set()
        active_futures = {}
        
        # Lock per proteggere le strutture dati del loop
        scheduling_lock = threading.Lock()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while len(completed_agents) + len(failed_agents) < len(self.agents):
                
                with scheduling_lock:
                    for agent in self.agents:
                        if agent.name in completed_agents or agent.name in failed_agents or agent.name in active_futures:
                            continue
                        
                        if all(dep in completed_agents for dep in agent.depends_on):
                            if any(dep in failed_agents for dep in agent.depends_on):
                                failed_agents.add(agent.name)
                                continue
                                
                            future = executor.submit(self.run_agent, agent, task, crew_context)
                            active_futures[agent.name] = future

                # Gestione completamento
                if active_futures:
                    done, _ = wait(list(active_futures.values()), return_when=FIRST_COMPLETED)
                    with scheduling_lock:
                        for agent_name, future in list(active_futures.items()):
                            if future in done:
                                try:
                                    future.result() # Qui il wrapper ha già salvato il risultato
                                    completed_agents.add(agent_name)
                                except Exception as e:
                                    logger.critical(f"[Crew] Critical Error in {agent_name}: {e}")
                                    failed_agents.add(agent_name)
                                del active_futures[agent_name]
                time.sleep(0.1)
        
        return crew_context["results"]

    def run_agent(self, agent, task, crew_context):
        """Esegue l'agente e salva centralmente il risultato."""
        output = agent.run(task, crew_context)
        with self.context_lock:
            crew_context["results"][agent.name] = output
        logger.info(f"[Crew] Result of {agent.name} saved")