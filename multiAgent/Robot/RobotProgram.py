from multiAgent.Robot.RobotInput import *

class RobotProgram:

    def __init__(self, robot, method,target=0):
        self.robot = robot;
        self.method = method;
        self.robotInput = RobotInput(method,target)