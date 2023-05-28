import collections
from typing import List
from multiAgent.helper.Point import *
#from org.apache.commons.collections15 import Transformer
from multiAgent.helper.Part import *
from multiAgent.Robot.Robot import *
from multiAgent.Robot.RobotLLC import *

#from bsh import This
#from edu.uci.ics.jung.algorithms.shortestpath import DijkstraShortestPath
#from edu.uci.ics.jung.graph import DirectedSparseGraph
#from intelligentProduct import ProductAgent
#from repast.simphony.engine.environment import RunEnvironment
#from repast.simphony.engine.schedule import ISchedule, ScheduleParameters, ScheduledMethod
#from repast.simphony.space.grid import Grid
from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *
from multiAgent.helper.Graph import *

class RobotAgent(ResourceAgent):
    def __init__(self, name: str, robot: RobotLLC,tableLocationObject):
        self.robot = robot
        self.working = False
        self.program = None
        
        # Capabilities Graph
        #self.robotCapabilities = DirectedSparseGraph[ProductState, ResourceEvent]()
        self.runningEdge = None
        self.robotCapabilities = DirectedSparseGraph()#DirectedSparseGraph<ProductState, ResourceEvent>
        #self.weightTransformer = Transformer[ResourceEvent, int](
        #    lambda edge: edge.getEventTime()
        #)
        
        # Neighbors
        self.neighbors = []
        self.tableNeighborNode = {}
        self.tableLocationObject = tableLocationObject
        
        self.createOutputGraph()
        #self.RAschedule = RASchedule()

    # Adding/getting neighbors for this resource
    def addNeighbor(self, neighbor: ResourceAgent):
        self.neighbors.append(neighbor)

    def getNeighbors(self) -> List[ResourceAgent]:
        return self.neighbors

    def getSchedule(self):
        return self.RAschedule
    
    def requestScheduleTime(self, productAgent, edge, startTime, endTime):
        edgeOffset = edge.getEventTime() - self.get_capabilities().find_edge(edge.getParent(), edge.getChild()).getEventTime()
        return self.RAschedule.addPa(productAgent, startTime+edgeOffset, endTime, False)
    
    def removeScheduleTime(self, productAgent, startTime, endTime):
        return self.RAschedule.removePa(productAgent, startTime, endTime)

    # ===========================================================================
    # Product agent communication
    # ===========================================================================
    def get_capabilities(self):
        return self.robotCapabilities           

    def createOutputGraph(self):
        # Helper method to create the capabilities graph for the part
        #For each program in the Robot LLC, create an edge 

        print(self.robot.getProgramList())
        for i, program in enumerate(self.robot.getProgramList()):

            print(program,program[4],program[5])


            endpoints = self.robot.getProgramEndpoints(program)

            print('endpoints',endpoints)
            start = endpoints[0]
            end = endpoints[1]
            center = self.robot.getRobot().getCenter()

            # Create the physical property of being in each location
            startLocation = PhysicalProperty(start)
            endLocation = PhysicalProperty(end)

            # Create the capability nodes
            #print(startLocation.getPoint())

            startNode = ProductState(self.tableLocationObject[tuple(startLocation.getPoint())], PhysicalProperty('pos'+program[4]), startLocation)
            endNode = ProductState(self.tableLocationObject[tuple(endLocation.getPoint())], PhysicalProperty('pos'+program[5]), endLocation)

            # Estimate the weight (time it takes to move between two points) using the manhattan distance.
            # Multiplier to give more time to the robot to perform the action
            distTravel = abs(center[0]-start[0]) + abs(center[1]-start[1]) + abs(start[0]-end[0]) + abs(start[1]-end[1]) + abs(center[0]-end[0]) + abs(center[1]-end[1])
            pickPlaceOffset = 15
            weight = int(distTravel/self.robot.getRobot().getVelocity()) + pickPlaceOffset

            # Create and add the edge to the capabilities
            programEdge = ResourceEvent(startNode, endNode, program, weight)
            self.robotCapabilities.addEdge(programEdge,startNode, endNode)


    def findNeighborNodes(self):
        # Finds at which nodes the neighbors are connected
        self.tableNeighborNode = {}

        # Fill the lookup table that matches the neighbor with the node
        for neighbor in self.neighbors:
            for node in self.robotCapabilities.nodes():
                if neighbor.getCapabilities().has_node(node):
                    # Assume only one node can be shared between neighbors
                    self.tableNeighborNode[neighbor] = node
###

    
    # ===========================================================================
    # Product agent communication
    # ===========================================================================
    
    def get_capabilities(self):
        return self.robotCapabilities
        
    def query(self, queriedEdge, productAgent):
        #Find the desired edge
        desiredEdge = None
        for robotEdge in self.getCapabilities().getEdges():
            if robotEdge.getActiveMethod() == queriedEdge.getActiveMethod():
                desiredEdge = robotEdge
                break
        #Find the offset between the queried edge and when the actual program should be run
        edgeOffset = queriedEdge.getEventTime() - self.getCapabilities().findEdge(queriedEdge.getParent(), queriedEdge.getChild()).getEventTime()
        schedule = RunEnvironment.getInstance().getCurrentSchedule()
        startTime = schedule.getTickCount() + edgeOffset

        #If the product agent is scheduled for this time, run the desired program at that time;
        if desiredEdge != None and self.RAschedule.checkPATime(productAgent, int(startTime), int(startTime + desiredEdge.getEventTime())):
            #Schedule it for the future
            schedule.schedule(ScheduleParameters.createOneTime(startTime),
                self.robot, "runMoveObjectProgram", [queriedEdge.getActiveMethod(), productAgent.getPartName()])
            self.informPA(productAgent, queriedEdge)
            return True

        return False
