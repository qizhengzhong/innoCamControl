from typing import List, Tuple
from multiAgent.helper.Point import *
#from java.lang.reflect import Method
#from repast.simphony.engine.schedule import ScheduledMethod
from multiAgent.Robot.RobotProgram import *

class RobotLLC:
    def __init__(self, robot):
        self.robot = robot
        self.program_list = []
        self.program_run = []
        self.working = False
        self.part_name = None

        #self.populate_methods(robot)

        self.moveToMethod=0
        self.homeMethod=1
        self.pickUpMethod=2
        self.placeObjectMethod=3

    def writeMoveObjectProgram(self, name, a, b, object_type):
        program = Program(name, a, b)

        # Move to where the object is
        moveTo1 = RobotProgram(self.robot, self.moveToMethod, a)
        program.add(moveTo1)

        # Pick up the object
        pickObject = RobotProgram(self.robot, self.pickUpMethod, object_type)
        program.add(pickObject)

        # Move back
        moveCenter = RobotProgram(self.robot, self.homeMethod)
        program.add(moveCenter)

        # Move where you want the object to be
        moveTo2 = RobotProgram(self.robot, self.moveToMethod, b)
        program.add(moveTo2)

        # Place the object
        place = RobotProgram(self.robot, self.placeObjectMethod)
        program.add(place)

        # Move back
        program.add(moveCenter)

        self.program_list.append(program)

    def getRobot(self):
        return self.robot

    def getProgramList(self):
        return [program.getName() for program in self.program_list]

    def getProgramEndpoints(self, program_name):
        for program in self.program_list:
            if program.getName() == program_name:
                return program.getStart(), program.getEnd()
        return None

    def getVelocity(self):
        return self.robot.getVelocity()    

class Program:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.subProgramList = []
        
    def add(self, robotProgram):
        self.subProgramList.append(robotProgram)

    def getName(self):
        return self.name

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getProgramList(self):
        return self.subProgramList
