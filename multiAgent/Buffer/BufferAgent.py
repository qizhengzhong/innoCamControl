#from typing import List
from collections import defaultdict

#import networkx as nx
#from networkx.classes.digraph import DiGraph

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *

from multiAgent.Buffer.BufferLLC import *
from multiAgent.helper.DijkstraGraph import *
from multiAgent.helper.Graph import *
from multiAgent.resourceAgent.ResourceAgent import *
from multiAgent.resourceAgent.ResourceAgentHelper import *

class BufferAgent(ResourceAgent):
    def __init__(self, name: str, buffer_name: BufferLLC):
        self.buffer = buffer_name
        self.bufferCapabilities = DirectedSparseGraph()#DirectedSparseGraph<ProductState, ResourceEvent>

        self.neighbors = [] #ArrayList<ResourceAgent>
        self.tableNeighborNode = {} #HashMap<ResourceAgent, ProductState>
        self.weightTransformer = 0 #Transformer<ResourceEvent, Integer>
        self.RAschedule = RASchedule(self)
        self.createOutputGraph()

    def addNeighbor(self, neighbor: ResourceAgent):
        self.neighbors.append(neighbor)

    def getNeighbors(self) -> List[ResourceAgent]:
        return self.neighbors

    def getSchedule(self) -> RASchedule:
        return self.RAschedule

    def requestScheduleTime(self, productAgent, edge: ResourceEvent, startTime: int, endTime: int) -> bool:
        return True

    def removeScheduleTime(self, productAgent, startTime: int, endTime: int) -> bool:
        return True

    def getCapabilities(self):
        return self.bufferCapabilities
    
    #need to add productAgent
    def teamQuery(self, desiredProperty: PhysicalProperty, currentNode: ProductState, maxTime: int, bid, currentTime: int):
        ResourceAgentHelper().teamQuery(desiredProperty, currentNode, maxTime, bid, currentTime, self, self.neighbors, self.tableNeighborNode, self.bufferCapabilities, self.weightTransformer)

    def query(self, queriedEdge: ResourceEvent, productAgent) -> bool:

        print('query received')
        # No need to check if the part is on RAschedule since it's a buffer
        #program = queriedEdge.getActiveMethod()
        program="F12"
        # If the queried program is true,
        if program == "End":
            return True

        # Find the desired edge
        desiredEdge = None
        for edge in self.getCapabilities().getEdges():
            if edge.getActiveMethod() == program:
                desiredEdge = edge
                break

        # Find the relevant position
        point = program[1:]

        tokens = point.split(",")

        x = 100#int(tokens[0])
        y = 100#int(tokens[1])


        # Obtain the program
        programType = program[0]

        # Run the corresponding program
        if programType == 'F':
            if self.buffer.moveFromStorage(productAgent.getPartName(), Point(x, y)) == True:
                # Let the part know that the edge is done
                self.informPA(productAgent, desiredEdge)
                return True

        elif programType == 'T':
            if self.buffer.moveToStorage(productAgent.getPartName(), Point(x, y)):
                # Let the part know that the edge is done
                self.informPA(productAgent, desiredEdge)
                return True

        return False


    def informPA(self, productAgent, edge: ResourceEvent):
        # Using the edge of the weight (might need to check with Robot LLC in the future)
        schedule = RunEnvironment.getInstance().getCurrentSchedule()

        systemOutput = DirectedSparseGraph()
        systemOutput.addEdge(edge, edge.getParent(), edge.getChild())
        occuredEvents = [edge]

        schedule.schedule(ScheduleParameters.createOneTime(schedule.getTickCount() + edge.getEventTime()), productAgent,
                          "informEvent", [systemOutput, edge.getChild(), occuredEvents])


    def getCapabilities(self):
        return self.bufferCapabilities

    # Helper methods
    def createOutputGraph(self):
        storageLocation = PhysicalProperty(self.buffer.getStoragePoint())
        storageNode = ProductState(self.buffer.getBuffer(), PhysicalProperty('storage'), storageLocation)

        for enterPoints in self.buffer.getEnterPoints():
            #Create the node for being at the enter point

            print('enterPoints',enterPoints)
            enterLocation = PhysicalProperty(enterPoints)
            enterNode = ProductState(self.buffer.getBuffer(), PhysicalProperty('enter'), enterLocation)
           
            #Program to move it FROM storage. Format: Fx,y
            programOutEdge = ResourceEvent(storageNode, enterNode, "F" + str(enterNode.getLocation()[0]) + "," + str(enterNode.getLocation()[1]), 1)
            self.bufferCapabilities.addEdge(programOutEdge, storageNode, enterNode)
            
            #Program to move TO storage. Format: Tx,y
            programInEdge = ResourceEvent(enterNode, storageNode, "T" + str(enterNode.getLocation()[0]) + "," + str(enterNode.getLocation()[1]), 1)
            self.bufferCapabilities.addEdge(programInEdge, enterNode, storageNode)

            #Program to move hold at storage. Format: Tx,y
            holdEdge = ResourceEvent(storageNode, storageNode, "S" + str(storageNode.getLocation()[0]) + "," + str(storageNode.getLocation()[1]), 1)
            self.bufferCapabilities.addEdge(holdEdge, storageNode, storageNode)


    def findNeighborNodes(self) -> None:
        self.tableNeighborNode = HashMap[ResourceAgent, ProductState]()

        for neighbor in self.neighbors:
            for node in self.bufferCapabilities.getVertices():
                if neighbor.getCapabilities().containsVertex(node):
                    self.tableNeighborNode.put(neighbor, node)
