from typing import List
from collections import namedtuple
from itertools import chain
from multiAgent.helper.Graph import *

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *

class EnvironmentModel(DirectedSparseGraph):
    """
    Beliefs
    Unlike the product history, which represents past states of the
    physical part, the environment model represents the reachable states of the physical part.
    """
    def __init__(self, currentState):
        super().__init__()
        self.currentState = None
        self.dummyEmptyNode = ProductState(None, None, PhysicalProperty(Point(18, 60)))  # random point
        self.startingEdge = ResourceEvent(self.dummyEmptyNode, currentState, None, 0)
        self.addEdge(self.startingEdge, self.dummyEmptyNode, currentState)
        

    def update(self, systemOutput, currentState):
        self.currentState = currentState
        self.updateSystemOutput(systemOutput)

    def updateSystemOutput(self, systemOutput):
        for event in systemOutput.getEdges():
            self.addEdge(event, event.getParent(), event.getChild())
        for state in systemOutput.getVertices():
            self.addVertex(state)

    def updateCurrentState(self, currentState):
        self.addVertex(currentState)
        self.currentState = currentState

    def getCurrentState(self):
        return self.currentState

    def clear(self):
        remove_vertices = []
        remove_edges = []
        for node in self.getVertices():
            if not (self.current_state == node or self.current_state == self.dummy_empty_node):
                remove_vertices.append(node)

        for edge in self.getEdges():
            if edge != self.starting_edge:
                remove_edges.append(edge)

        for node in remove_vertices:
            self.removeVertex(node)
        for edge in remove_edges:
            self.removeEdge(edge)

        remove_vertices.clear()
        remove_edges.clear()
        remove_vertices = None
        remove_edges = None

    def isEmpty(self):
        return all(edge == self.startingEdge for edge in self.getEdges())
