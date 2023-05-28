from multiAgent.helper.Point import *
#from repast.simphony.engine.schedule import ScheduledMethod

class MachineLLC:
    def __init__(self, machine): 
        self.machine = machine
        self.currentPart = None
        self.started = False
        self.done = False
        self.programList = []
        
        for i in range(1, 7):
            processEnabled = machine.getProcessesEnabled()[i - 1]
            if processEnabled:
                self.programList.append(Program("S" + str(i), i - 1, machine.getProcessTime(i - 1)))
    
    
    def getMachine(self):
        return self.machine

    def getLocation(self):
        return self.machine.getCenter()


    def getProgramList(self):
        programString = []
        
        for program in self.programList:
            programString.append(program.getProgramName())
        
        return programString

    def getProgramTime(self, programName):
        for program in self.programList:
            if program.getProgramName() == programName:
                return program.getProcessTime()
        
        return -1

#-------------------not used------------------
    def runProgram(self, manProcess: str, partName: str):
        if manProcess == "S1":
            if machine.S1(partName):
                self.started = True
                return True
        elif manProcess == "S2":
            if machine.S2(partName):
                self.started = True
                return True
        elif manProcess == "S3":
            if machine.S3(partName):
                self.started = True
                return True
        elif manProcess == "S4":
            if machine.S4(partName):
                self.started = True
                return True
        elif manProcess == "S5":
            if machine.S5(partName):
                self.started = True
                return True
        elif manProcess == "S6":
            if machine.S6(partName):
                self.started = True
                return True
        elif manProcess == "Hold":
            if not self.machine.getStatus():
                return True
        
        return False

    def checkPresence(self):
        if self.machine.getPartHere() is None:
            self.started = False
            return
        elif not self.machine.getPartHere() == self.currentPart:
            self.currentPart = self.machine.getPartHere()
            self.started = False

    def doNothing(self):
        pass
    
    def getTimeLeft(self):
        return self.machine.getTimeLeft()
    
    def queryWorking(self):
        return self.machine.getStatus()
    
    def queryDone(self):
        self.done = self.machine.getPartHere() is not None and not self.queryWorking() and self.started
        return self.done
    
    def resetStarted(self):
        self.started = False

class Program:
    def __init__(self, programName: str, processIndex: int, processTime: int):
        self.programName = programName
        self.processIndex = processIndex
        self.processTime = processTime
    
    def getProgramName(self):
        return self.programName
    
    def getProcessIndex(self):
        return self.processIndex
    
    def getProcessTime(self):
        return self.processTime
