from typing import List
from multiAgent.helper.Point import *
from multiAgent.helper.Part import *
#from repast.simphony.space.grid import Grid

class Buffer:
    def __init__(self, name: str, enterPoints: List[Point], storagePoint: Point):
        self.name = name
        self.enterPoints = enterPoints
        self.storagePoint = storagePoint
        self.partList = []
    
    def getStoragePoint(self):
        return self.storagePoint

    def getEnterPoints(self):
        return self.enterPoints


    def moveToStorage(self, partName: str, enterPoint: Point):
        #for obj in self.grid.getObjectsAt(enterPoint.x, enterPoint.y):
        #    if isinstance(obj, Part) and obj.__str__() == partName:
        #        self.grid.moveTo(obj, self.storagePoint.x, self.storagePoint.y)
        #        return True
        return False

    def moveFromStorage(self, partName: str, exitPoint: Point):
        #for obj in self.grid.getObjectsAt(self.storagePoint.x, self.storagePoint.y):
        #    if isinstance(obj, Part) and obj.__str__() == partName:
        #        self.grid.moveTo(obj, exitPoint.x, exitPoint.y)
        #       return True
        return False