import logging
from crewai import Crew, Agent

from Agents.LanguageDetector import LanguageDetector
from Agents.TechStackDetector import TechStackDetector
from Agents.ArchitectureDetector import ArchitectureDetector
from Agents.UseCaseDetector import UseCaseDetector
from Agents.APIExtractor import APIExtractor
from Agents.FeatureDetector import FeatureDetector
from Agents.VersionDetector import VersionDetector
from Agents.ReleasePolicyDetector import ReleasePolicyDetector
from Agents.BugFixChangeDetector import BugFixChangeDetector
from Agents.UseCaseDetector import RolesActorsUsecasesDetector

from Agents.Test.DummyAgent import DummyAgent


logger = logging.getLogger("main")

AGENTS = [
    LanguageDetector(),
    DummyAgent()
]

crew = Crew(
    agents=AGENTS,
    process="sequential",
    verbose=True
)