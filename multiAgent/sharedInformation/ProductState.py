from typing import List
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.helper.Point import *

class ProductState:
    def __init__(self, holdingObject, processCompleted, location):
        self.holdingObject = holdingObject
        self.processCompleted = processCompleted
        self.location = location
        

    def getLocation(self):
        return self.location.getPoint()


    def getProcessCompleted(self):
        if self.processCompleted is None or self.processCompleted.getProcessCompleted() is None:
            return "nothing completed"
        
        return self.processCompleted.getProcessCompleted()
    
    def getPhysicalProperties(self):
        lst = []
        
        if self.location is not None:
            lst.append(self.location)
            
        if self.processCompleted is not None:
            lst.append(self.processCompleted)
            
        return lst       