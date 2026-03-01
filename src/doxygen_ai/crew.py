from crewai import Crew

class DoxygenCrew(Crew):
    def __init__(self):
        super().__init__(agents=[], process="sequential", verbose=True)