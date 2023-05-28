import collections
from typing import List

from multiAgent.sharedInformation.ResourceEvent import *
from multiAgent.helper.Graph import *

class PAPlan:
    def __init__(self):
        self.plannedString = []
        self.startTimes = []
        self.endTimes = []


    def addEvent(self, event: ResourceEvent, startTime: int, endTime: int) -> bool:
        if startTime < 0:
            print("Start time is wrong for " + str(self.productAgent) + " for " + str(event))
            return False

        if len(self.plannedString) == 0:
            self.startTimes.append(startTime)
            self.endTimes.append(endTime)
            self.plannedString.append(event)
            return True

        checkStartTime = None
        for i in range(len(self.startTimes)):
            checkStartTime = self.startTimes[i]
            if checkStartTime < startTime:
                self.plannedString.insert(i, event)
                self.startTimes.insert(i, startTime)
                self.endTimes.insert(i, endTime)
                self.sortByStartTime()
                return True

        self.plannedString.append(event)
        self.startTimes.append(startTime)
        self.endTimes.append(endTime)
        self.sortByStartTime()
        return True

    def sortByStartTime(self):
        newStartList = sorted(self.startTimes)
        newEndList = []
        newPlannedString = []
        for sortIndex in range(len(newStartList)):
            startTimeSorted = newStartList[sortIndex]
            index = self.startTimes.index(startTimeSorted)
            newEndList.append(self.endTimes[index])
            newPlannedString.append(self.plannedString[index])
        self.startTimes = newStartList
        self.endTimes = newEndList
        self.plannedString = newPlannedString

    def removeEvent(self, event: ResourceEvent, startTime: int, endTime: int) -> bool:
        for index in range(len(self.startTimes)):
            if startTime >= self.startTimes[index] and endTime < self.endTimes[index] and event == self.plannedString[index]:
                self.startTimes.pop(index)
                if endTime >= self.endTimes[index]:
                    self.endTimes.pop(index)
                    self.plannedString.pop(index)
                else:
                    self.startTimes.insert(index, endTime)
                return True
        return False

    def getIndexOfNextEvent(self, event: ResourceEvent, currentTime: int) -> int:
        for index in range(len(self.plannedString) - 1):
            if self.plannedString == self.plannedString[index]:
                if currentTime >= self.startTimes[index] and currentTime <= self.startTimes[index + 1]:
                    return index + 1
        print("No " + str(event) + " planned for " + str(self.productAgent))
        return -1

    def getIndexOfNextEventByTime(self, time: int) -> int:
        for i in range(len(self.startTimes)):
            startTime = self.startTimes[i]
            if startTime >= time:
                return i
        return -1
        
    def getIndexEvent(self, index):
        if index >= 0 and index < len(self.planned_string):
            return self.planned_string[index]
        return None

    def getIndexStartTime(self, index):
        if index >= 0:
            return self.start_times[index]
        return -1

    def getIndexEndTime(self, index):
        if index >= 0:
            return self.end_times[index]
        return -1

    def isEmpty(self, time):
        if self.getIndexOfNextEventByTime(time) == -1:
            return True
        return False
