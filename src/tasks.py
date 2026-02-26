from crewai import Task
import logging

logger = logging.getLogger("main")



def language_detection_task(agent, src, template):
    return Task(
        description="Detect project languages",
        expected_output="Language analysis JSON",
        agent=agent,
        input_files={
            "src": src,
            "template": template
        }
    )