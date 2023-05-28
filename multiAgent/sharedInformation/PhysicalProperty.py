
class PhysicalProperty:
    def __init__(self, value):
        if isinstance(value,str):
            self.processCompleted = value
        else:
            self.point = value
        
    def getPoint(self):
        return self.point

    def getProcessCompleted(self):
        return self.processCompleted
