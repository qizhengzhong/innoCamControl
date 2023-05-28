#from typing import List
from collections import defaultdict

#import networkx as nx
#from networkx.classes.digraph import DiGraph

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *

from multiAgent.Machine.MachineLLC import *
from multiAgent.helper.DijkstraGraph import *
from multiAgent.helper.Graph import *
from multiAgent.resourceAgent.ResourceAgent import *


class MachineAgent(ResourceAgent):
    def __init__(self, name, machine:MachineLLC):
        self.name = name
        self.machine = machine
        self.working = False
        self.program = 0

        self.runningEdge = None #ResourceEvent        
        self.machineCapabilities = DirectedSparseGraph()#DirectedSparseGraph<ProductState, ResourceEvent>

        self.neighbors = [] #ArrayList<ResourceAgent>
        self.tableNeighborNode = {} #HashMap<ResourceAgent, ProductState>
        self.weightTransformer = 0 #Transformer<ResourceEvent, Integer>
        #self.RAschedule = RASchedule()
        self.createOutputGraph()
    

    def addNeighbor(self, neighbor: ResourceAgent):
        self.neighbors.append(neighbor)

    def getNeighbors(self):
        return self.neighbors

    def getSchedule(self) -> RASchedule:
        return self.RAschedule


    def createOutputGraph(self):
        #Node representing the part located in the CNC
        #print(self.machine.getLocation(),self.machine.getMachine())
        machineLocation = PhysicalProperty(self.machine.getLocation())
        startNode = ProductState(self.machine.getMachine(), PhysicalProperty('Idle'), machineLocation)
        selfEdge = ResourceEvent(startNode, startNode, "Hold", 1);
        self.machineCapabilities.addEdge(selfEdge,startNode, startNode)
        #Nodes that represent machining operations performed on the part
        #print(self.machine.getProgramList())
        print('programList',self.machine.getProgramList())
        for program in self.machine.getProgramList():
            #print(program)
            #Create the node representing this program being complete
            print('program',program[1:])
            programName = PhysicalProperty(program[1:])
            programNode = ProductState(self.machine.getMachine(), programName, machineLocation)
            
            #Create the edge to go to this node
            programEdge = ResourceEvent(startNode, programNode, program, self.machine.getProgramTime(program))
            self.machineCapabilities.addEdge(programEdge, startNode, programNode)

            #Create the edge to come back to the original position
            programReset = ResourceEvent(programNode, startNode, "Reset", 0)
            self.machineCapabilities.addEdge(programReset, programNode, startNode)

    def findNeighborNodes(self):
        self.tableNeighborNode = {}

        for neighbor in self.neighbors:
            for node in self.machineCapabilities.getVertices():
                if neighbor.getCapabilities().containsVertex(node):
                    self.tableNeighborNode[neighbor] = node

