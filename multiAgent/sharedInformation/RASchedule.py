from typing import List
#from intelligentProduct import ProductAgent
from multiAgent.resourceAgent.ResourceAgent import *
from collections import deque


class RASchedule:
    def __init__(self, resourceAgent):
        self.resourceAgent = resourceAgent
        self.productAgents = []
        self.startTimes = []
        self.endTimes = []

    def __str__(self):
        total = ""
        for i in range(len(self.productAgents)):
            total += " " + self.productAgents[i] + " [" + str(self.startTimes[i]) + "," + str(self.endTimes[i]) + "];"
        return str(self.resource_agent) + "Schedule:" + total

    def checkPaTime(self, productAgent, startTime: int, endTime: int) -> bool:
        productAgentName = str(productAgent)

        for i in range(len(self.startTimes)):  
            checkStartTime = self.startTimes[i]
            checkEndTime = self.endTimes[i]

            if startTime >= checkStartTime and endtime <= checkEndTime:
                if self.productAgents[i] == productAgentName:
                    return True
                else:
                    return False
        return False

    def addPa(self, productAgent, startTime: int, endTime: int, allowMultiple: bool) -> bool:
        productAgentName = str(productAgent)

        if startTime < 0 or endTime <= 0 or endTime < startTime:
            print("End time and start time are wrong for " + str(self.resourceAgent) + " for " + productAgentName)
            return False

        if not self.productAgents:
            self.productAgents.append(productAgentName)
            self.startTimes.append(startTime)
            self.endTimes.append(endTime)
            self.sortByStartTime()
            return True

        if not allowMultiple:
            for i in range(len(self.startTimes) - 1):
                checkStartTime = self.startTimes[i]
                checkEndTime = self.endTimes[i]

                if startTime <= checkEndTime:
                    if endTime <= checkStartTime:
                        self.productAgents.insert(i, productAgentName)
                        self.startTimes.insert(i, startTime)
                        self.endTimes.insert(i, endTime)
                        self.sortByStartTime()
                        return True
                    else:
                        print("Resource busy " + str(self.resourceAgent) + " for " + productAgentName)
                        return False

        self.productAgents.append(productAgentName)
        self.startTimes.append(startTime)
        self.endTimes.append(endTime)
        self.sortByStartTime()
        return True

    #def removePa(self, productAgent, startTime: int, endTime: int) -> bool:
    #    product_agent_name = str(productAgent)

    #    for i in range(len(self.startTimes)):
    #        if startTime >= self.startTimes[i] and startTime < self.endTimes[i] and productAgentName == self.productAgents[i]:
    #            self.productAgents.pop(i)
    #            self.startTimes.pop(i)
    #            self.endTimes.pop(i)
    #            return True
    #    return False

    def sortByStartTime(self) -> None:
        newStartList = self.startTimes.copy()
        newEndList = self.endTimes.copy()
        newPa = self.productAgents.copy()
        
        newStartList.sort()
        for sortIndex in range(len(newStartList)):
            startTimeSorted = newStartList[sortIndex]
            index = self.startTimes.index(startTimeSorted)
            newEndList[sortIndex] = self.endTimes[index]
            newPa[sortIndex] = self.productAgents[index]
        
        self.startTimes = newStartList
        self.endTimes = newEndList
        self.productAgents = newPa

    def removePa(self, productAgent, startTime: int, endTime: int) -> bool:
        productAgentName = str(productAgent)
        for index in range(len(self.startTimes)):
            # Find if there is a product agent scheduled for the proposed time to remove it
            if startTime >= self.startTimes[index] and startTime < self.endTimes[index] and productAgentName == self.productAgents[index]:
                # Remove the product agent if the proposed scheduled agent is found
                self.startTimes.pop(index)

                # Check if the desired end time is after the indexed end time
                if endTime >= self.endTimes[index]:
                    self.endTimes.pop(index)
                    self.productAgents.pop(index)
                # If it is not, just shorten the length of the event by moving the start time to the proposed endTime
                else:
                    self.startTimes.insert(index, endTime)

                self.sortByStartTime()
                return True

        return False

    def getFreeTimeAmount(self, startTime: int) -> int:
        # Large number if there is nothing after this part
        ret = 100000
        for i in range(len(self.startTimes)):
            if self.startTimes[i] > startTime:
                # The time until the first product agent is scheduled to arrive
                if i == 0:
                    ret = self.startTimes[i] - startTime
                # Check to see that the last event ended
                elif self.endTimes[i-1] <= startTime:
                    ret = self.startTimes[i] - startTime
                # The resource is working during this time
                else:
                    ret = 0
                break
        
        return ret

    def getNextFreeTime(self, startTime: int, timeAction: int) -> int:
        # If there are no end times or it's after all the scheduled events, return the start time
        if len(self.endTimes) == 0 or startTime > self.endTimes[-1]:
            return startTime

        checkEndTime = startTime + timeAction
        # Check to see if the resource is working
        for i in range(len(self.startTimes)):
            if self.startTimes[i] > startTime + checkEndTime:
                if i == 0 or self.endTimes[i-1] < startTime:
                    return startTime

        return self.endTimes[-1] + 1