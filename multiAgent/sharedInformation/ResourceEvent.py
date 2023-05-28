from multiAgent.sharedInformation.ProductState import *
from multiAgent.resourceAgent.ResourceAgent import *

class ResourceEvent:
    
    def __init__(self, parent: ProductState, child: ProductState, activeMethod: str, eventTime: int):
        self.parent = parent
        self.child = child
        
        #self.eventAgent = agent
        self.activeMethod = activeMethod        
        self.eventTime = eventTime
        
        self.controllability = False
        self.observability = False
    

    def getParent(self) -> ProductState:
        return self.parent
    
    def getChild(self) -> ProductState:
        return self.child
    
    def getEventTime(self) -> int:
        return self.eventTime
        
    def getActiveMethod(self) -> str:
        return self.activeMethod
    
    def getEventAgent(self) -> ResourceAgent:
        return self.eventAgent
    
    def setWeight(self, weight: int):
        self.eventTime = weight
    
    def setChild(self, child: ProductState):
        self.child = child
    
    def setControllability(self, controllability: bool):
        self.controllability = controllability
    
    def setObservability(self, observability: bool):
        self.observability = observability
    
    def getControllability(self) -> bool:
        return self.controllability
    
    def getObservability(self) -> bool:
        return self.observability