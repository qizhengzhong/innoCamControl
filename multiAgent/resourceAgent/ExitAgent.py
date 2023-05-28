from typing import List
#from repast.simphony.space.grid import Grid, GridPoint
from intelligentProduct.ProductAgent import * 

from resourceAgent.Robot import *
from resourceAgent.RobotLLC import *

from sharedInformation.ResourceEvent import *
from sharedInformation.ProductState import *
from sharedInformation.PhysicalProperty import *
from sharedInformation.RASchedule import *

from helper.Graph import DirectedSparseGraph
#from org.apache.commons.collections15 import Transformer


class ExitAgent:
    def __init__(self, name: str, robot: Robot, exit_event_name: str):
        self.robot = robot
        #self.grid = physical_grid
        self.exit_event_name = exit_event_name
    
    def query(self, exit_event: ResourceEvent, product_agent: ProductAgent) -> bool:
        if 'exit' in exit_event.getActiveMethod():
            for obj in self.grid.getObjects():
                if product_agent.getPartName() in obj.__str__():
                    point: GridPoint = self.grid.getLocation(obj)
                    self.grid.moveTo(self.robot, point.getX()+2, point.getY())
                    
                    schedule: ISchedule = RunEnvironment.getInstance().getCurrentSchedule()
                    schedule.schedule(ScheduleParameters.createOneTime(schedule.getTickCount()+1), self.grid,
                                    "moveTo", [obj, [self.robot.getCenter().x-4, self.robot.getCenter().y]])
                    schedule.schedule(ScheduleParameters.createOneTime(schedule.getTickCount()+1), self.grid,
                                    "moveTo", [self.robot, [self.robot.getCenter().x, self.robot.getCenter().y]])
        return True
    
    def getExitEventName(self) -> str:
        return self.exit_event_name

    def __str__(self) -> str:
        return "Exit Agent"

    #================================================================================
    # Product agent scheduling
    #================================================================================

    def getSchedule(self) -> RASchedule:
        return None

    def requestScheduleTime(self, product_agent: ProductAgent, edge: ResourceEvent, startTime: int, endTime: int) -> bool:
        return True

    def removeScheduleTime(self, product_agent: ProductAgent, startTime: int, endTime: int) -> bool:
        return True
    
    #================================================================================
    # Product agent communication
    #================================================================================

    def getCapabilities(self) -> DirectedSparseGraph:
        return None

    def addNeighbor(self, neighbor: ResourceAgent):
        pass

    def getNeighbors(self) -> List[ResourceAgent]:
        return None

    def teamQuery(self, product_agent: ProductAgent, desired_property: PhysicalProperty,
                current_node: ProductState, max_time: int, bid: DirectedSparseGraph,
                current_time: int):
        pass
