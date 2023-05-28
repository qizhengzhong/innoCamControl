from Machine.Machine import *
from Machine.MachineLLC import *
from Machine.MachineAgent import *

from Buffer.Buffer import *
from Buffer.BufferLLC import *
from Buffer.BufferAgent import *

from Robot.Robot import *
from Robot.RobotLLC import *
from Robot.RobotAgent import *

from resourceAgent.ExitAgent import *
#from helper import 
import matplotlib.pyplot as plt

from helper.Point import *
from helper.PartCreatorforBuffer import *

def buildProductionControl():


    tableLocationObject = {}
    listMachineLLC = [] # List of all of Machine controllers
    listBufferLLC = [] #List of all of Buffer Controllers
    listRobotLLC = []

    listMachineAgent=[] # List of all Machine agents
    listBufferAgent = [] #List of all Buffer agents
    listRobotAgent = []

    # Machine locations
    machineTAPoint = [30,100]
    machineTBPoint = [50,90]
    machineTCPoint = [30,80]
    machineTDPoint = [50,40]
    machineTEPoint = [30,30]
    machineTFPoint = [50,20]
    machineTGPoint = [70,100]
    machineTHPoint = [70,80]
    machineTIPoint = [90,100]
    machineTJPoint = [90,80]
    machineTKPoint = [70,40]
    machineTLPoint = [70,20]
    machineTMPoint = [90,40]
    machineTNPoint = [90,20]
    machineTOPoint = [110,100]
    machineTPPoint = [130,90]
    machineTQPoint = [110,80]
    machineTRPoint = [130,40]
    machineTSPoint = [110,30]
    machineTTPoint = [130,20]

    machineLocations = [machineTAPoint, machineTBPoint, 
                            machineTCPoint, machineTDPoint, machineTEPoint, 
                            machineTFPoint, machineTGPoint, machineTHPoint, 
                            machineTIPoint, machineTJPoint, machineTKPoint, 
                            machineTLPoint, machineTMPoint, machineTNPoint, 
                            machineTOPoint, machineTPPoint, machineTQPoint, 
                            machineTRPoint, machineTSPoint, machineTTPoint]
    
    scale = 2
    # Time for processes
    S1time = 75 * scale
    S2time = 30 * scale
    S3time = 55 * scale
    S4time = 50 * scale
    S5time = 85 * scale
    S6time = 10 * scale

   # Machine Times
    machineTATime = [S1time, -1, -1, -1, S5time, -1]
    machineTBTime = [S1time, -1, -1, -1, S5time, -1]
    machineTCTime = [S1time, -1, -1, -1, S5time, -1]
    machineTDTime = [S1time, -1, -1, -1, S5time, -1]
    machineTETime = [S1time, -1, -1, -1, S5time, -1]
    machineTFTime = [S1time, -1, -1, -1, S5time, -1]
    machineTGTime = [S1time, -1, -1, -1, S5time, -1]
    machineTHTime = [S1time, -1, -1, -1, S5time, -1]
    machineTITime = [-1, -1, S3time, -1, -1, S6time]
    machineTJTime = [-1, -1, S3time, -1, -1, S6time]
    machineTKTime = [-1, -1, S3time, -1, -1, S6time]
    machineTLTime = [-1, -1, S3time, -1, -1, S6time]
    machineTMTime = [-1, S2time, -1, S4time, -1, -1]
    machineTNTime = [-1, S2time, -1, S4time, -1, -1]
    machineTOTime = [-1, S2time, -1, S4time, -1, -1]
    machineTPTime = [-1, S2time, -1, S4time, -1, -1]
    machineTQTime = [-1, S2time, -1, S4time, -1, -1]
    machineTRTime = [-1, S2time, -1, S4time, -1, -1]
    machineTSTime = [-1, S2time, -1, S4time, -1, -1]
    machineTTTime = [-1, S2time, -1, S4time, -1, -1]

    machineTimes = [
        machineTATime, machineTBTime, machineTCTime,
        machineTDTime, machineTETime, machineTFTime,
        machineTGTime, machineTHTime, machineTITime,
        machineTJTime, machineTKTime, machineTLTime,
        machineTMTime, machineTNTime, machineTOTime,
        machineTPTime, machineTQTime, machineTRTime,
        machineTSTime, machineTTTime
    ]

    # Machines
    for index in range(len(machineLocations)):
        nameSuffix = chr(65 + index)
        machine = Machine("machineT" + nameSuffix, machineLocations[index], 0, machineTimes[index])
        machineLLC = MachineLLC(machine)
        listMachineLLC.append(machineLLC)
        tableLocationObject[tuple(machineLocations[index])] = machine


    # Machines
    for machineLLC in listMachineLLC:
        machineAgent = MachineAgent(str(machineLLC.getMachine()) + " Agent", machineLLC)
        listMachineAgent.append(machineAgent)
    #================================================================================
    # Buffers
    #================================================================================


    # Storage points for bay buffers
    exitPoint= [18,60]
    exitPointStorage= [142,60]
    depositB1Point= [40,70]
    depositB2Point= [40,50]
    depositB3Point = [80,70]
    depositB4Point = [80,50]
    depositB5Point = [120,70]
    depositB6Point = [120,50]
    buffer1Point = [60,60]
    buffer2Point = [100,60]
    
    # Enter points for bay buffers
    enterPoint = [20,60]
    depositB1PointEnter = [40,68]
    depositB2PointEnter = [40,52]
    depositB3PointEnter = [80,68]
    depositB4PointEnter = [80,52]
    depositB5PointEnter = [120,68]
    depositB6PointEnter = [120,52]
    buffer1PointEnter = [58,60]
    buffer2PointEnter = [98,60]
    
    # Exit points for bay buffers
    exitBufferEnter = [140,60]
    depositB1PointExit = [40,72]
    depositB2PointExit = [40,48]
    depositB3PointExit = [80,72]
    depositB4PointExit = [80,48]
    depositB5PointExit = [120,72]
    depositB6PointExit = [120,48]
    buffer1PointExit = [62,60]
    buffer2PointExit = [102,60]
    
    bufferLocations= [exitPoint, exitPointStorage, depositB1Point, 
                                                   depositB2Point, depositB3Point, depositB4Point, 
                                                   depositB5Point, depositB6Point, buffer1Point, 
                                                   buffer2Point]



    bufferEnterLocations = [[enterPoint], [exitBufferEnter], [depositB1PointEnter, depositB1PointExit],
    [depositB2PointEnter, depositB2PointExit], [depositB3PointEnter, depositB3PointExit], [depositB4PointEnter, depositB4PointExit],
    [depositB5PointEnter, depositB5PointExit], [depositB6PointEnter, depositB6PointExit], [buffer1PointEnter, buffer1PointExit], [buffer2PointEnter, buffer2PointExit]]
    # Buffer names
    bufferNames = ["EnterBuffer", "ExitBuffer", "depositB1", "depositB2", "depositB3", "depositB4", "depositB5", "depositB6", "buffer1234", "buffer3456"]
 

    # Buffers
    for index in range(len(bufferLocations)):
        buffer1 = Buffer(bufferNames[index], bufferEnterLocations[index], bufferLocations[index])
        bufferLLC = BufferLLC(buffer1)
        listBufferLLC.append(bufferLLC)
        tableLocationObject[tuple(bufferLocations[index])] = buffer1
        for point in bufferEnterLocations[index]:
            tableLocationObject[tuple(point)] = buffer1
          
    # Buffer
    for bufferLLC in listBufferLLC:
        bufferAgent = BufferAgent(str(bufferLLC.getBuffer()) + " Agent", bufferLLC)
        listBufferAgent.append(bufferAgent)




    # Robots
    # Speed of the robots
    robotSpeed = 20

    robotB1Point = [40,90]
    robotB2Point = [40,30]
    robotB3Point = [80,90]
    robotB4Point = [80,30]
    robotB5Point = [120,90]
    robotB6Point = [120,30]
    robotM12Point = [40,60]
    robotM34Point = [80,60]
    robotM56Point = [120,60]

    # Robot names
    robotNames = ["RobotB1", "RobotB2", "RobotB3", "RobotB4", "RobotB5", "RobotB6", "RobotM12", "RobotM34", "RobotM56"]

    # Points where the robots should go
    robotLocations = [robotB1Point, robotB2Point, robotB3Point, robotB4Point, robotB5Point, robotB6Point, robotM12Point, robotM34Point, robotM56Point]

    # Points that the robots can move between
    robotB1PointMove = [depositB1PointExit, machineTAPoint, machineTBPoint, machineTCPoint]
    robotB2PointMove = [depositB2PointExit, machineTDPoint, machineTEPoint, machineTFPoint]
    robotB3PointMove = [depositB3PointExit, machineTGPoint, machineTHPoint, machineTIPoint, machineTJPoint]
    robotB4PointMove = [depositB4PointExit, machineTKPoint, machineTLPoint, machineTMPoint, machineTNPoint]
    robotB5PointMove = [depositB5PointExit, machineTOPoint, machineTPPoint, machineTQPoint]
    robotB6PointMove = [depositB6PointExit, machineTRPoint, machineTSPoint, machineTTPoint]
    robotM12PointMove = [enterPoint, depositB1PointEnter, depositB2PointEnter, buffer1PointEnter]
    robotM34PointMove = [buffer1PointExit, depositB3PointEnter, depositB4PointEnter, buffer2PointEnter]
    robotM56PointMove = [buffer2PointExit, depositB5PointEnter, depositB6PointEnter, exitBufferEnter]
    # Where the robots can move things between
    robotNeighborLocations = [
        robotB1PointMove, robotB2PointMove, robotB3PointMove,
        robotB4PointMove, robotB5PointMove, robotB6PointMove,
        robotM12PointMove, robotM34PointMove, robotM56PointMove
    ]

    # The index of the MACHINE neighbors for each of the robots
    robotB1MachineIndex = [0, 1, 2]
    robotB2MachineIndex = [3, 4, 5]
    robotB3MachineIndex = [6, 7, 8, 9]
    robotB4MachineIndex = [10, 11, 12, 13]
    robotB5MachineIndex = [14, 15, 16]
    robotB6MachineIndex = [17, 18, 19]
    robotM12MachineIndex = []
    robotM34MachineIndex = []
    robotM56MachineIndex = []

    # The index of the MACHINE neighbors for all of the robots
    robotMachineNeighborIndices = [
        robotB1MachineIndex, robotB2MachineIndex, robotB3MachineIndex,
        robotB4MachineIndex, robotB5MachineIndex, robotB6MachineIndex,
        robotM12MachineIndex, robotM34MachineIndex, robotM56MachineIndex
    ]

    # The index of the BUFFER neighbors for each of the robots
    robotB1BufferIndex = [2]
    robotB2BufferIndex = [3]
    robotB3BufferIndex = [4]
    robotB4BufferIndex = [5]
    robotB5BufferIndex = [6]
    robotB6BufferIndex = [7]
    robotM12BufferIndex = [0, 2, 3, 8]
    robotM34BufferIndex = [4, 5, 8, 9]
    robotM56BufferIndex = [1, 6, 7, 9]

    # The index of the BUFFER neighbors for all of the robots
    robotBufferNeighborIndices = [
        robotB1BufferIndex, robotB2BufferIndex, robotB3BufferIndex,
        robotB4BufferIndex, robotB5BufferIndex, robotB6BufferIndex,
        robotM12BufferIndex, robotM34BufferIndex, robotM56BufferIndex
    ]



    for i in machineLocations:
        plt.plot(i[0], i[1], 'ro')

    for i in bufferLocations:
        plt.plot(i[0], i[1], 'bo')
    
    for i in bufferEnterLocations:
        for j in i:
            plt.plot(j[0], j[1], 'go')

    for i in robotLocations:
        plt.plot(i[0], i[1], 'yo')     

    for i in robotNeighborLocations:   
        for j in i:
            plt.plot(j[0], j[1], 'mo')     

    physicalGrid={}
    
    plt.show() 


    # Robots
    for index in range(len(robotLocations)):
        robot = Robot(robotNames[index], robotLocations[index], robotSpeed, 25)
        robotLLC = RobotLLC(robot)
        locationAmount = len(robotNeighborLocations[index])
        for j in range(locationAmount):
            for k in range(locationAmount):
                if j != k:
                    robotLLC.writeMoveObjectProgram(f"move{j}{k}", robotNeighborLocations[index][j], robotNeighborLocations[index][k], "Part")
                    pass
        listRobotLLC.append(robotLLC)

        #print('robotLocations',robotLocations[index])
        tableLocationObject[tuple(robotLocations[index])] = robot

    print('tableLocationObject',tableLocationObject.keys())


    for robotLLC in listRobotLLC:
        #print(robotLLC.get_robot())
        robotAgent = RobotAgent(str(robotLLC.getRobot()) + " Agent", robotLLC,tableLocationObject)  
        listRobotAgent.append(robotAgent)

    # The location of the exit human
    exitHumanLocation = [10, 10]
    exitHumanPoint = [6, 10]
    #exitHumanAgent = ExitAgent()
    #partCreatora = PartCreatorforBuffer()


    #Exit Robot (and Agent)
    exitHumanRobot = Robot("exitHuman", exitHumanLocation, 200, 200)
    exitHumanAgent = ExitAgent("exitHumanAgent", exitHumanRobot, "exit")
    exitHumanAgent=[]


#def buildPartCreator(self, physicalContext, physicalGrid, cyberContext):
    # Some of the parameters for the part creator
    startTime = 5
    partCreatingInterval = 120
    startingBuffer = listBufferLLC[0].getBuffer()
    startingBufferAgent = listBufferAgent[0]
    
    # Create and add this part creator to the cyber context
    partCreatora = PartCreatorforBuffer(startingBuffer, startingBufferAgent,
                                            exitHumanAgent, startTime, partCreatingInterval)

   
            
    # Resource agents neighbors
    print('robotLocations',robotLocations)
    print('robotMachineNeighborIndices',robotMachineNeighborIndices)
    for index, robotLocation in enumerate(robotLocations):
        robotAgent = listRobotAgent[index]
        robotMachineIndices=robotMachineNeighborIndices[index]
        robotBufferIndices = robotBufferNeighborIndices[index]
        
        # Machine agents neighbor population
        print('robotMachineIndices',robotMachineIndices)
        for machineIndex in robotMachineIndices:
            machineAgent = listMachineAgent[machineIndex]

            robotAgent.addNeighbor(machineAgent)
            machineAgent.addNeighbor(robotAgent)
            
        # Buffer agents neighbor population
        for bufferIndex in robotBufferIndices:
            bufferAgent = listBufferAgent[bufferIndex]
            robotAgent.addNeighbor(bufferAgent)
            bufferAgent.addNeighbor(robotAgent)


    print('finish')
# Creates the machines, robots, and buffers
buildProductionControl()

