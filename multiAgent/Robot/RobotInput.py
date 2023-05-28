from multiAgent.helper.Point import *

class RobotInput:
    def __init__(self, destination, object_type):
        self.destination = destination
        self.object_type = object_type
        
    def getDestination(self):
        return self.destination
        
    def getObjectType(self):
        return self.object_type
