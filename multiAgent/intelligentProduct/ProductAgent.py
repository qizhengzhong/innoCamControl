from typing import List

from multiAgent.helper.Graph import *
from multiAgent.resourceAgent.ResourceAgent import *

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *


class ProductAgent:
    def getPartName(self):
        pass

    #================================================================================
    # PA to PA communication
    #================================================================================

    def getPriority(self):
        pass

    def rescheduleRequest(self, resourceAgent: ResourceAgent, startTime: int):
        pass

    #================================================================================
    # RA to PA communication
    #================================================================================

    def informEvent(self, systemOutput: DirectedSparseGraph, currentState: ProductState, occuredEvents: List[ResourceEvent]):
        pass

    def submitBid(self, bid: DirectedSparseGraph):
        pass

    def updateEdge(self, rescheduleEdge: ResourceEvent):
        pass
