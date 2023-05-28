from typing import List
from multiAgent.helper.Point import Point
from multiAgent.helper.Part import Part
#from repast.simphony.space.grid import Grid

class BufferLLC:
    def __init__(self, buffer1):
        self.buffer = buffer1

    def getBuffer(self):
        return self.buffer

    def getStoragePoint(self):
        return self.buffer.getStoragePoint()

    def getEnterPoints(self):
        return self.buffer.getEnterPoints()

    def moveToStorage(self, part_name: str, enter_point: Point):
        flag = False
        for point in self.buffer.getEnterPoints():
            if enter_point == point:
                flag = True
                break
        if not flag:
            return False
        return self.buffer.moveToStorage(part_name, enter_point)

    def moveFromStorage(self, part_name: str, enter_point: Point):
        flag = False
        for point in self.buffer.getEnterPoints():
            if enter_point == point:
                flag = True
                break
        if not flag:
            return False
        return self.buffer.moveFromStorage(part_name, enter_point)