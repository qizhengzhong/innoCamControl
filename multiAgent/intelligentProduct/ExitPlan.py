 # Converted Python class

from multiAgent.resourceAgent import ResourceAgent
from multiAgent.sharedInformation import ResourceEvent

class ExitPlan:
    def __init__(self, exitRA: ResourceAgent, exitEvent: ResourceEvent):
        self.exitRA = exitRA
        self.exitEvent = exitEvent
        
    def getExitRA(self):
        return self.exitRA
    
    def getExitEvent(self):
        return self.exitEvent
    
    def __str__(self):
        return "Exit Event: " + str(self.exitEvent) + " - " + str(self.exitRA)
