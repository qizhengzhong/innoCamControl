import math
import numpy as np


#from edu.uci.ics.jung.graph import DirectedSparseGraph




#from intelligentProduct import ExitPlan
#from intelligentProduct import ProductAgentInstance
#from intelligentProduct import ProductionPlan

#from resourceAgent.Buffer import *
#from resourceAgent.BufferAgent import * 
#from resourceAgent import ExitAgent
from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.sharedInformation.ProductState import * 
from multiAgent.sharedInformation.PhysicalProperty import * 

from multiAgent.resourceAgent.RFIDTag import *
from multiAgent.helper.Part import * 
from multiAgent.intelligentProduct.ProductAgentInstance import *

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
        self.productAgent=self.startPartAgentCreation()

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

        startingNode = ProductState(self.buffer,PhysicalProperty('buffer0'), PhysicalProperty(storagePoint))
        productAgentInstance = ProductAgentInstance(part, startingNode, 0, self.getProductionPlan(self.partType), self.getExitPlan(self.partType))

        bid = DirectedSparseGraph()
        #newEvent = ResourceEvent(self.bufferAgent, startingNode, startingNode, None, 0)
        newEvent = ResourceEvent(startingNode, startingNode, 'None', 0)
        bid.addEdge(newEvent, newEvent.getParent(), newEvent.getChild())
        eventList = []
        eventList.append(newEvent)
        productAgentInstance.informEvent(bid, newEvent.getChild(), eventList)
        #productAgentInstance.setPANumber(self.PAnumber)

        #self.cyberContext.add(productAgentInstance)
        self.numberofParts += 1

        return productAgentInstance

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

    def getProductAgent(self):
        return self.productAgent
    


