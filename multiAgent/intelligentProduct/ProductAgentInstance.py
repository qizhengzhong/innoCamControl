from typing import List
from collections import defaultdict
from queue import PriorityQueue

from multiAgent.intelligentProduct.EnvironmentModel import *
from multiAgent.intelligentProduct.ExitPlan import *
from multiAgent.intelligentProduct.PAPlan import *
from multiAgent.intelligentProduct.ProductAgent import *
from multiAgent.intelligentProduct.ProductHistory import *
from multiAgent.intelligentProduct.ProductionPlan import *

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import *
from multiAgent.sharedInformation.PhysicalProperty import *
from multiAgent.sharedInformation.RASchedule import *

from multiAgent.helper.Graph import *
from multiAgent.helper.Part import *

from multiAgent.Buffer.Buffer import *
from multiAgent.Buffer.BufferAgent import *
from multiAgent.Buffer.BufferLLC import *

class ProductAgentInstance(ProductAgent):
    explorationWaitTime = 1
    planningWaitTime = 1

    def __init__(self, part: Part, startingNode: ProductState, priority: int, productionPlan: ProductionPlan, exitPlan: ExitPlan):
        self.partName = str(part)
        self.PANumber = -1
        self.priority = priority

        # Initialize the Knowledge Base
        self.productionPlan = productionPlan  # Production Plan
        self.exitPlan = exitPlan
        self.productHistory = ProductHistory(startingNode)  # Product History
        self.environmentModel = EnvironmentModel(startingNode)  # Environment Model
        self.plan = PAPlan()  # Agent Plan

        # Set the starting node in the belief model
        self.environmentModel.updateCurrentState(startingNode)

        # No edge queried
        self.queriedEdge = None


    def setPANumber(self, number):
        self.PANumber = number

    def __str__(self):
        return f"PA{self.PANumber} for {self.partName}"

    def getPartName(self):
        return self.partName

    # Decision Director - Working with KB

    def updateEnvironmentModelState(self, currentState: ProductState):
        #print('currentState',currentState.getProcessCompleted())
        self.environmentModel.updateCurrentState(currentState)

    def updateProductHistory(self, systemOutput: DirectedSparseGraph, currentState: ProductState,
                             occuredEvents: List[ResourceEvent]):
        self.productHistory.update(systemOutput, currentState, occuredEvents)

    # Decision Director - Intelligence

    def requestNewPlan(self):

        print("self.getDesiredProperties()",self.getDesiredProperties())
        for prop in self.getDesiredProperties():
            print(prop.getProcessCompleted())
        print('fiish ')
        
        self.startExploration(self.productHistory, self.getDesiredProperties())

        # Set the next time for execution
        #self.nextExecutionStartTime = int(self.explorationWaitTime + self.planningWaitTime)

        # Wait for one time step and then check the output of the exploration
        #nextTimeStep = self.explorationWaitTime
        #self.simulationSchedule.schedule(ScheduleParameters.createOneTime(nextTimeStep),
        #                                  self, "checkExploration", [])

        #self.checkExploration()

    def checkExploration(self): #call_back functions
        #if not self.newEnvironmentModel.isEmpty():
        if self.newEnvironmentModel.isEmpty(): #for test
            self.environmentModel.clear()
            self.environmentModel.update(self.newEnvironmentModel, self.newEnvironmentModel.getCurrentState())
            self.newEnvironmentModel.clear()
            self.startPlanning(self.getDesiredProperties(), self.environmentModel, self.plan)
            #self.simulationSchedule.schedule(ScheduleParameters.createOneTime(self.nextExecutionStartTime), self, "checkPlanning", [self])
            self.checkPlanning()
        else:
            print(f"Could not find {self.getDesiredProperties()} for {self.partName}")
            #self.sendExitPlan()

        print("finish checkExploration")    
            
    def checkPlanning(self):
        #if not self.newPlan.isEmpty(int(1)):
        if self.newPlan.isEmpty(int(1)): #for test
            self.plan = self.newPlan
            self.startExecution(self.plan)
        else:
            self.sendExitPlan()
            
    def sendExitPlan(self):
        currentTime = int(1)
        exitPAPlan = PAPlan(self)
        for i in range(3):
            exitPAPlan.addEvent(self.exitPlan.getExitEvent(), currentTime + i, currentTime + i + 1)
        self.startExecution(exitPAPlan)
    
    def startExploration(self, productHistory, desiredProperties):

        #print('desiredProperties',desiredProperties)
        currentState = productHistory.getCurrentState()
        self.newEnvironmentModel = EnvironmentModel(currentState)
        bidTime = self.getStartBidTime()

        #send message out
        #while self.newEnvironmentModel.isEmpty() and bidTime <= self.getMaxBidTime():
        
        for i in range(1):#for debug replace while
            #contactRA=productHistory.getLastEvent().getEventAgent() #modify here seperate RA and PA

            #print('contactRA',contactRA)
            #for test
            buffer1 = Buffer("EnterBuffer", [[20,60]], [18,60])
            bufferLLC = BufferLLC(buffer1)
            contactRA = BufferAgent(str(bufferLLC.getBuffer()) + " Agent", bufferLLC)
            #for test

            nextTimeQuery = int(self.explorationWaitTime + self.planningWaitTime)
            
            for desiredProperty in desiredProperties:
                print('desiredProperty',desiredProperty.getProcessCompleted())
                print('currentState',currentState.getProcessCompleted())
                
                bid = DirectedSparseGraph()
                bid.addVertex(currentState)
                contactRA.teamQuery(desiredProperty, currentState, bidTime, bid, nextTimeQuery)

                #change MQTT send message
            bidTime += self.getBidTimeChange()

        print('finish startExploration')
    
    def submitBid(self, bid):
        self.newEnvironmentModel.update(bid)
    
    def getStartBidTime(self):
        return 300
    
    def getBidTimeChange(self):
        return 500
    
    def getMaxBidTime(self):
        return 10000
    
    def startPlanning(self, desiredProperties, environmentModel, plan):
        bestPath = self.getBestPath(desiredProperties, environmentModel)
        currentTime = int(1)
        newPlanAttempt = PAPlan()
        time = self.nextExecutionStartTime
        epsilon = 2
        scheduleBound = min(self.getMaxScheduledEvents(), len(bestPath))
        for i in range(scheduleBound):
            scheduleEvent = bestPath[i]
            eventEndTime = time + scheduleEvent.getEventTime()
            newPlanAttempt.addEvent(scheduleEvent, time, time + scheduleEvent.getEventTime() + epsilon)
            time = eventEndTime
        self.removeScheduledEvents(currentTime, plan)
     
        #Schedule all of the events in the new plan
        badPathFlag = self.scheduleEvents(currentTime,newPlanAttempt)
        
        if not badPathFlag:
            removeScheduledEvents(currentTime,newPlanAttempt)
            newPlanAttempt = PAPlan(this)
                
        self.newPlan = newPlanAttempt
    
    def removeScheduledEvents(self, currentTime, plan):
        for i in range(plan.getPlanSize() - 1, -1, -1):
            event = plan.getEvent(i)
            if event.getEndTime() > currentTime:
                plan.removeEvent(event)
    
    def getMaxScheduledEvents(self):
        return 0
        
    def removeScheduledEvents(self, time, plan) -> bool:
        nextPlannedEventIndex = plan.getIndexOfNextEventByTime(time)
        nextEvent = plan.getIndexEvent(nextPlannedEventIndex)
        flag = True
        while nextEvent is not None:
            if not nextEvent.getEventAgent().removeScheduleTime(
                self, plan.getIndexStartTime(nextPlannedEventIndex),
                plan.getIndexEndTime(nextPlannedEventIndex)
            ):
                flag = False
            nextPlannedEventIndex += 1
            nextEvent = plan.getIndexEvent(nextPlannedEventIndex)
        return flag

    def scheduleEvents(self, time, plan) -> bool:
        nextPlannedEventIndex = plan.getIndexOfNextEventByTime(time)
        nextEvent = plan.getIndexEvent(nextPlannedEventIndex)
        flag = True
        while nextEvent is not None:
            if not nextEvent.getEventAgent().requestScheduleTime(
                self, nextEvent,
                plan.getIndexStartTime(nextPlannedEventIndex), plan.getIndexEndTime(nextPlannedEventIndex)
            ):
                flag = False
            nextPlannedEventIndex += 1
            nextEvent = plan.getIndexEvent(nextPlannedEventIndex)
        return flag

    def updateEdge(self, rescheduleEdge):
        self.requestNewPlan()

    def getBestPath(self, desiredProperties: List[PhysicalProperty], environmentModel: EnvironmentModel) -> List[ResourceEvent]:
        shortestPathGetter = DijkstraShortestPath(environmentModel, self.getWeightTransformer())
        shortestPathGetter.reset()
        dist = 999999999
        desiredNodeFinal = None
        desiredNodes = []
        for property in desiredProperties:
            for node in environmentModel.getVertices():
                if property in node.getPhysicalProperties():
                    desiredNodes.append(node)
        for desiredNode in desiredNodes:
            compareDist = shortestPathGetter.getDistanceMap(environmentModel.getCurrentState()).get(desiredNode).intValue()
            if compareDist < dist:
                dist = compareDist
                desiredNodeFinal = desiredNode
        return shortestPathGetter.getPath(environmentModel.getCurrentState(), desiredNodeFinal)


    def getWeightTransformer(self):
        pass
        #return Transformer[ResourceEvent, int]({
        #    "transform": lambda edge: edge.getEventTime()
        #})

    def informEvent(self, systemOutput: DirectedSparseGraph, 
                    currentState: ProductState, occuredEvents: List[ResourceEvent]):
        # Update the models
        self.updateEnvironmentModelState(currentState)
        self.updateProductHistory(systemOutput, currentState, occuredEvents)

        print('initialize En model and Pro history')
        # If there is no next action, find a new plan
        if self.plan.isEmpty(1):
            print("requestNewPlan")            
            self.requestNewPlan()
        else:
            self.startExecution(self.plan)


    def startExecution(self, plan: PAPlan):
        nextIndex = plan.getIndexOfNextEventByTime(int(1))
        nextAction = plan.getIndexEvent(nextIndex)

        # Find the event time
        nextEventTime = plan.getIndexStartTime(nextIndex)

        # Schedule querying the resource for the next action
        #self.simulationSchedule.schedule(ScheduleParameters.createOneTime(nextEventTime),
        #                                  self, "queryResource", [nextAction.getEventAgent(), nextAction])
       
        print('nextAction',nextAction) 


        #for test
        buffer1 = Buffer("EnterBuffer", [[20,60]], [18,60])
        bufferLLC = BufferLLC(buffer1)
        contactRA = BufferAgent(str(bufferLLC.getBuffer()) + " Agent", bufferLLC)
        #for test

        #self.queryResource(nextAction.getEventAgent(),nextAction)

        self.queryResource(contactRA,'F12')
        print('finish Execution')


    def queryResource(self, resourceAgent: ResourceAgent, edge: ResourceEvent):
        # Set the queried edge
        self.queriedEdge = edge
        queried = resourceAgent.query(edge, self)

        #if not queried:
        #    self.sendExitPlan()
        #    print(f"{self} query did not work for {resourceAgent} {edge}")


    def getDesiredProperties(self) -> List[PhysicalProperty]:
        incompleteProperties = []
        # Obtain the states that have occurred on the physical product using the product history
        checkStates = [event.getChild() for event in self.productHistory.getOccurredEvents()]
        # Compare the production plan to the occurred states
        for partSet in self.productionPlan.getSetList():
            highestIndex = -1  # the highest index when a desired property occurred
            print('desiredProperty',partSet)
            # For each desired physical property
            for desiredProperty in partSet:
                # Check if it has occurred
                propertyComplete = False
                for index in range(len(checkStates)):
                    if desiredProperty in checkStates[index].getPhysicalProperties():
                        # If it's occurred, overwrite the highest index, if appropriate
                        if index > highestIndex:
                            highestIndex = index
                        propertyComplete = True
                        break

                # Add to incomplete properties if the property hasn't previously occurred in the product history
                if not propertyComplete:
                    incompleteProperties.append(desiredProperty)
            # If there are incomplete properties, then return these
            if incompleteProperties:
                break
            # If there aren't incomplete properties, then go onto the next set of properties
            # Note: need to remove all of the properties that are associated with the previous set to continue
            else:
                for j in range(highestIndex):
                    checkStates.pop(0)

        return incompleteProperties


    def getPriority(self):
        return self.priority


    def rescheduleRequest(self, resourceAgent: ResourceAgent, startTime: int):
        pass


    def getProductHistory(self) -> List[ResourceEvent]:
        return self.productHistory.getOccurredEvents()


