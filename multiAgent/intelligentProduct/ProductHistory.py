from typing import List
import numpy as np
from abc import ABC, abstractmethod

from multiAgent.helper.Point import *
from multiAgent.helper.Graph import *


from multiAgent.intelligentProduct.ProductAgentInstance import *

from multiAgent.resourceAgent.ResourceAgent import *
from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *

class ProductHistory(DirectedSparseGraph):
    #dummyEmptyNode: ProductState # Empty node needed to represent the "parent" of the initial state.
    #startingEdge: ResourceEvent
    #occurredEvents: List[ResourceEvent]

    def __init__(self, currentState: ProductState):
        super().__init__()
        self.dummyEmptyNode = ProductState(None, None, PhysicalProperty(Point(18,60))) # random point
        self.currentState = currentState
        self.startingEdge = ResourceEvent(self.dummyEmptyNode, currentState, None, 0)
        self.addEdge(self.startingEdge, self.dummyEmptyNode, currentState)
        self.occurredEvents = [self.startingEdge]
        
    def update(self, systemOutput: DirectedSparseGraph, 
               currentState: ProductState, occurredEvents: List[ResourceEvent]):
        #Update both the graph and the current state
        self.updateCurrentState(currentState)
        self.updateSystemOutput(systemOutput, occurredEvents)
        
    def updateSystemOutput(self, systemOutput: DirectedSparseGraph, 
               occurredEvents: List[ResourceEvent]):
        #Update directed graph
        for event in systemOutput.getEdges():
            self.addEdge(event, event.getParent(), event.getChild())
        for state in systemOutput.getVertices():
            self.addVertex(state)
        
        #Update list of occurred events
        self.occurredEvents.extend(occurredEvents)
        
    def updateCurrentState(self, currentState: ProductState):
        self.addVertex(currentState)
        self.currentState = currentState
        
    def getCurrentState(self) -> ProductState:
        return self.currentState
        
    def getOccurredEvents(self) -> List[ResourceEvent]:
        return self.occurredEvents
        
    def getLastEvent(self) -> ResourceEvent:
        return self.occurredEvents[-1]
