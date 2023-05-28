from typing import List
from abc import ABC, abstractmethod
from multiAgent.helper.Part import *
#from intelligentProduct import ProductAgent
#from edu.uci.ics.jung.graph import DirectedSparseGraph

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *

class ResourceAgent():
    
    #================================================================================
    # Setting up local neighbors
    #================================================================================
    
    #@abstractmethod
    def addNeighbor(self, neighbor: 'ResourceAgent') -> None:
        pass
    
    #@abstractmethod
    def getNeighbors(self) -> List['ResourceAgent']:
        pass
    
    #================================================================================
    # PA to RA Communication
    #================================================================================
    
    #@abstractmethod
    def teamQuery(self, productAgent, desiredProperty: PhysicalProperty, bidPartState: ProductState, maxTime: int, existingBid, currentTime: int) -> None:
        pass
    
    #@abstractmethod
    def requestScheduleTime(self, productAgent, edge, startTime: int, endTime: int) -> bool:
        pass
    
    #abstractmethod
    def removeScheduleTime(self, productAgent, startTime: int, endTime: int) -> bool:
        pass
    
    #@abstractmethod
    def query(self, desiredEdge, productAgent) -> bool:
        pass
    
    #================================================================================
    # RA to RA communication
    #================================================================================
    
    #@abstractmethod
    def getSchedule(self) -> RASchedule:
        pass
    
    #@abstractmethod
    def getCapabilities(self):
        pass
