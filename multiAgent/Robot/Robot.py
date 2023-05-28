from typing import List
from multiAgent.helper.Point import Point
#from java.util import ArrayList
#from repast.simphony.context import Context
#from repast.simphony.space.grid import Grid
#from repast.simphony.util import ContextUtils
from multiAgent.helper.Part import *
from multiAgent.Robot.RobotInput import *

class Robot:
    def __init__(self, name:str, center:Point, vel:int, radius:int):
        self.name = name
        #self.grid = grid
        self.vel = vel
        self.radius = radius
        self.center = center
        
        self.end = center
        self.pathFollow = []
        self.working = False
        self.holdingObject = False
        self.heldObject = None
        
    def getCenter(self):
        return self.center


    def getVelocity(self):
        return self.vel

#---------------not used ------

    def moveTo(self, input:RobotInput):
        pass

    def home(self, input:RobotInput):
        pass

    def pickUp(self, input:RobotInput, partName:str):
        pass

    def placeObject(self, input:RobotInput):    
        pass

    def getStatus(self) -> bool:
        return not self.working
    
    def getPartHere(self) -> str:
        objectsHere = self.grid.getObjectsAt(self.end.x, self.end.y)
        for obj in objectsHere:
            if isinstance(obj, Part):
                return str(obj)
        return None


