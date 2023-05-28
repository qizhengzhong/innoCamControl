from multiAgent.helper.Point import *


class Machine:
    def __init__(self, name, location, rotation, processTimes):
        self.name = name
        self.location = location
        self.processLocation = Point(location[0], location[1])
        
        self.working = False        
        self.processTimes = processTimes
        self.waitTimer = 0
        
        self.processesEnabled = [False] * 6
        self.rotation = rotation
        
        # Must have process times for all 6 stages of processing (if time is -1, process cannot be done)
        if len(processTimes) != 6:
            raise ValueError(f"Number of process times are wrong for {self}")
        else:
            # Fill out the processes enabled array
            for i in range(6):
                processTime = processTimes[i]
                if processTime <= 0:
                    self.processesEnabled[i] = False
                else:
                    self.processesEnabled[i] = True
                    
    def getProcessesEnabled(self):
        return self.processesEnabled

    def getProcessTime(self, i):
        return self.processTimes[i]

    def getCenter(self):
        return self.location

    def getRotation(self):
        return self.rotation
#---------------not called---------------------
    def setBroken(self):
        self.working = True
        self.waitTimer = 150000

    def getTimeLeft(self):
        return self.waitTimer

    def fix(self):
        self.working = False
        self.waitTimer = 0

    def machine(self):
        if self.working:
            self.waitTimer -= 1
            if self.waitTimer <= 0:
                self.fix()

    def setPart(self, part):
        if not self.working:
            if part is None:
                self.partName = None
                self.partSize = None
                self.partColor = None
                self.windingRule = None
                self.partShape = None
                return
            else:
                pass
                #self.partName = part.getName()
                #self.partSize = part.getSize()
                #self.partColor = part.getColor()
                #self.windingRule = part.getWindingRule()
                #self.partShape = GeneralPath(part.getShape())

    def doProcess(self, processNum):
        if not self.working:
            if not self.processesEnabled[processNum]:
                return False
            
            self.working = True
            self.waitTimer = self.processTimes[processNum]
            return True
        else:
            return False            

    def getStatus(self):
        return self.working

    def getPartHere(self):
        #objectsHere = self.grid.getObjectsAt(self.location.x, self.location.y)
        #for object in objectsHere:
        #    if isinstance(object, Part):
        #        return str(object)
        return None
#-------------------

    def S1(self, partName):
        if not self.processesEnabled[0] or self.getPartHere() is None:
            return False

        # Puts a black box on the part in the top left
        topleft = Path()
        topleft.moveTo(-1, 1)
        topleft.lineTo(-1, 0)

        self.partName = partName
        methodCalled = self.appendShape(MachineInput(topleft))

        if methodCalled:
            self.waitTimer = self.processTimes[0]
            self.move(partName, self.location, self.processLocation)
            return True

        return False

#-------------------
    def waiting(self):
        if self.waitTimer != 0:
            self.waitTimer -= 1
            if self.waitTimer == 0:
                self.move(partNameHere, self.processLocation, self.location)

    def move(self, partName, location, destination):
        pass
        #objectsHere = grid.getObjectsAt(location.x, location.y)
        #desiredObject = None
        #for object in objectsHere:
        #    if "Part" in object.__class__.__name__ and partName in str(object):
        #        desiredObject = object
        #        break
        #try:
        #    grid.moveTo(desiredObject, destination.x, destination.y)
        #except SpatialException as e:
        #    print("move didn't work for some reason")