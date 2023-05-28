import math
import numpy as np


#from edu.uci.ics.jung.graph import DirectedSparseGraph



#from intelligentProduct import ExitPlan
#from intelligentProduct import ProductAgentInstance
#from intelligentProduct import ProductionPlan

#from resourceAgent.Buffer import *
#from resourceAgent.BufferAgent import * 
#from resourceAgent import ExitAgent
from sharedInformation.ResourceEvent import *
from sharedInformation.ProductState import * 
from sharedInformation.PhysicalProperty import * 

from resourceAgent.RFIDTag import *
from helper.Part import * 
from intelligentProduct.ProductAgentInstance import *

class PartCreatorforBuffer:

    def __init__(self, bufferName, startingBufferPosition, exitRA, startTime, intervalTime):
        self.startTime = startTime
        self.intervalTime = intervalTime

        self.buffer = bufferName
        self.bufferPosition= startingBufferPosition

        #self.exitRA = exitRA
        #self.exitEvent = ResourceEvent(exitRA, None, None, exitRA.getExitEventName(), 1)

        self.partType = 'a'

        #schedule = RunEnvironment.getInstance().getCurrentSchedule()
        #schedule.schedule(ScheduleParameters.createRepeating(startTime, intervalTime), self, "startPartAgentCreation")

        
        self.PAnumber = -1
        self.maxNumberOfParts = 150
        self.numberofParts = 0

        self.exitPoint = Point(142, 60)
        self.exitHumanPointPlace = Point(6, 10)
        self.startPartAgentCreation()

    def startPartAgentCreation(self):
        if self.partType not in ('a', 'b', 'c') or self.numberofParts >= self.maxNumberOfParts:
            return

        currentFinishedPartCount = 0
        if currentFinishedPartCount > 50:
            return

        self.PAnumber += 1

        storagePoint = self.bufferPosition
        part = Part(RFIDTag(str(self.PAnumber), self.partType))
        print('part',part)

        startingNode = ProductState(self.buffer, None, PhysicalProperty(storagePoint))
        productAgentInstance = ProductAgentInstance(part, startingNode, 0, self.getProductionPlan(self.partType), self.getExitPlan(self.partType))

        bid = DirectedSparseGraph()
        #newEvent = ResourceEvent(self.bufferAgent, startingNode, startingNode, None, 0)
        newEvent = ResourceEvent(startingNode, startingNode, None, 0)
        bid.addEdge(newEvent, newEvent.getParent(), newEvent.getChild())
        eventList = []
        eventList.append(newEvent)
        productAgentInstance.informEvent(bid, newEvent.getChild(), eventList)
        productAgentInstance.setPANumber(self.PAnumber)

        #self.cyberContext.add(productAgentInstance)
        self.numberofParts += 1

    def getProductionPlan(self,partType):
        productionPlan = ProductionPlan()
        if partType == 'a':

            #productionPlan.add(PhysicalProperty("S1"))

            set1 = []
            set1.append(PhysicalProperty("S1"))
            productionPlan.addNewSet(set1)
            
            set2 = []
            set2.append(PhysicalProperty("S2"))
            productionPlan.addNewSet(set2)
            
            set3 = []
            set3.append(PhysicalProperty("S3"))
            productionPlan.addNewSet(set3)
            
            set4 = []
            set4.append(PhysicalProperty("S4"))
            productionPlan.addNewSet(set4)
            
            set5 = []
            set5.append(PhysicalProperty("S5"))
            productionPlan.addNewSet(set5)
            
            set6 = []
            set6.append(PhysicalProperty("S6"))
            productionPlan.addNewSet(set6)
            
            end = []
            end.append(PhysicalProperty("End"))
            productionPlan.addNewSet(end)

        return productionPlan

    def getExitPlan(self, partType):
        pass
        #return ExitPlan(exitRA, exitEvent)

    def setPartType(self, partType):
        self.partType = partType

    def setMaxNumberOfParts(self, maxNumberOfParts):
        self.maxNumberOfParts = maxNumberOfParts


if __name__ == "__main__":
    # The location of the exit human
    exitHumanLocation = [10, 10]
    exitHumanPoint = [6, 10]
    #exitHumanAgent = ExitAgent()
    #partCreatora = PartCreatorforBuffer()


    #Exit Robot (and Agent)
    #exitHumanRobot = Robot("exitHuman", exitHumanLocation, 200, 200)
    #exitHumanAgent = ExitAgent("exitHumanAgent", exitHumanRobot, "exit")
    exitHumanAgent=[]


#def buildPartCreator(self, physicalContext, physicalGrid, cyberContext):
    # Some of the parameters for the part creator
    startTime = 5
    partCreatingInterval = 120
    startingBuffer = "EnterBuffer"
    startingBufferPosition = [0,0]
    #startingBufferAgent = listBufferAgent[0]
    
    # Create and add this part creator to the cyber context
    partCreatora = PartCreatorforBuffer(startingBuffer,startingBufferPosition,exitHumanAgent, startTime, partCreatingInterval)

    print('finish')
