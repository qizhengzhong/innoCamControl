from multiAgent.Machine.Machine import *
from multiAgent.Machine.MachineLLC import *
from multiAgent.Machine.MachineAgent import *

from multiAgent.Buffer.Buffer import *
from multiAgent.Buffer.BufferLLC import *
from multiAgent.Buffer.BufferAgent import *

from multiAgent.Robot.Robot import *
from multiAgent.Robot.RobotLLC import *
from multiAgent.Robot.RobotAgent import *
from multiAgent.Robot.RobotAgent import *

from multiAgent.intelligentProduct.PartCreatorforBuffer import *
import json

def setupAgents():
    with open('simulatorJsonInput.json') as f:
        data = json.load(f)

    # Use the data from the JSON file
    #print(data)

    tableLocationObject = {}
    objectLocation={}
   
    listMachineLLC = [] # List of all of Machine controllers
    listBufferLLC = [] #List of all of Buffer Controllers
    listRobotLLC = []

    listMachineAgent=[] # List of all Machine agents
    listBufferAgent = [] #List of all Buffer agents
    listRobotAgent = []

    machineLocations=data['machineLocations']
    machineNames=data['machineNames']
    machineX=[]
    machineY=[]
    machineLocationsList=[]
    for i, machine in enumerate(machineLocations):
        #X,Y=machine.split(',')
        machineX.append(machine[0])
        machineY.append(machine[1])
        machineLocationsList.append([machine[0],machine[1]])
        objectLocation[machineNames[i]]=machine

    print('machineLocationsList',machineLocationsList)
    machineProcessTimes=data['machineTimes']
    machineTimesList=[]
    for time in machineProcessTimes:
        #change "" to list
        timeList=time.split(',')
        timeListInt=[int(x) for x in timeList]
        machineTimesList.append(timeListInt)

    # Machines
    for index in range(len(machineLocationsList)):
        nameSuffix = chr(65 + index)
        machine = Machine("machineT" + nameSuffix, machineLocationsList[index], 0, machineTimesList[index])
        machineLLC = MachineLLC(machine)
        machineAgent = MachineAgent(str(machineLLC.getMachine()) + " Agent", machineLLC)
        
        listMachineAgent.append(machineAgent)
        listMachineLLC.append(machineLLC)
        tableLocationObject[tuple(machineLocations[index])] = machine


   
    # Buffers
    bufferNames=data['bufferNames']
    bufferLocations=data['bufferLocations']
    bufferEnterName=data['bufferEnterName']
    bufferEnterLocations=data['bufferEnterLocations']
    bufferX=[]
    bufferY=[]
    bufferLocationsList=[]
    for i,buffer in enumerate(bufferLocations):
        bufferX.append(buffer[0])
        bufferY.append(buffer[1])
        bufferLocationsList.append([buffer[0],buffer[1]])
        objectLocation[bufferNames[i]]=buffer

    bufferEnterLocationsList=[]
    for i,bufferEnter in enumerate(bufferEnterLocations):
        bufferEnterLocationsList.append(bufferEnter)  
        for j,enter in enumerate(bufferEnter):
            objectLocation[bufferEnterName[i][j]]=enter

    for index in range(len(bufferLocationsList)):
        buffer1 = Buffer(bufferNames[index], bufferEnterLocationsList[index], bufferLocationsList[index])
        bufferLLC = BufferLLC(buffer1)
        listBufferLLC.append(bufferLLC)
        tableLocationObject[tuple(bufferLocations[index])] = buffer1
        for point in bufferEnterLocations[index]:
            tableLocationObject[tuple(point)] = buffer1
            bufferAgent = BufferAgent(str(bufferLLC.getBuffer()) + " Agent", bufferLLC)
            listBufferAgent.append(bufferAgent)

    
    # robot
    robotSpeed=20
    robotLocations=data['robotLocations']
    robotNames=data['robotNames']
    robotNeighborLocations=data['robotNeighborLocations']
    robotX=[]
    robotY=[]
    robotLocationsList=[]
    for i, robot in enumerate(robotLocations):
        #X,Y=robot.split(',')
        robotX.append(robot[0])
        robotY.append(robot[1])
        robotLocationsList.append([robot[0],robot[1]])
        objectLocation[robotNames[i]]=robot

    print('objectLocation',objectLocation)
    # Robots
    for index in range(len(robotLocations)):
        robot = Robot(robotNames[index], robotLocations[index], robotSpeed, 25)
        robotLLC = RobotLLC(robot)
        locationAmount = len(robotNeighborLocations[index])
        for j in range(locationAmount):
            for k in range(locationAmount):
                if j != k:
                    robotLLC.writeMoveObjectProgram(f"move{j}{k}", objectLocation[robotNeighborLocations[index][j]], objectLocation[robotNeighborLocations[index][k]], "Part")
                    print('move',robotNeighborLocations[index][j],robotNeighborLocations[index][k])
                    pass
        listRobotLLC.append(robotLLC)
        robotAgent = RobotAgent(str(robotLLC.getRobot()) + " Agent", robotLLC,tableLocationObject)  
        listRobotAgent.append(robotAgent)

        #print('robotLocations',robotLocations[index])
        tableLocationObject[tuple(robotLocations[index])] = robot

    print('tableLocationObject',tableLocationObject.keys())

    # The index of the MACHINE neighbors for all of the robots
    robotMachineNeighborIndices=data['robotMachineNeighborIndices']
    # The index of the BUFFER neighbors for all of the robots
    robotBufferNeighborIndices=data['robotBufferNeighborIndices']

    for index, robotLocation in enumerate(robotLocations):
        robotAgent = listRobotAgent[index]
        robotMachineIndices=robotMachineNeighborIndices[index]
        robotBufferIndices =robotBufferNeighborIndices[index]
        
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


#product

    # The location of the exit human
    exitHumanLocation = [10, 10]
    exitHumanPoint = [6, 10]
    #exitHumanAgent = ExitAgent()
    #partCreatora = PartCreatorforBuffer()


    #Exit Robot (and Agent)
    #exitHumanRobot = Robot("exitHuman", exitHumanLocation, 200, 200)
    #exitHumanAgent = ExitAgent("exitHumanAgent", exitHumanRobot, "exit")
    exitHumanAgent=[]


#def buildPartCreator(self, physicalContext, physicalGrid, cyberContext):
    # Some of the parameters for the part creator
    startTime = 5
    partCreatingInterval = 120
    startingBuffer = "EnterBuffer"
    startingBufferPosition = [0,0]
    #startingBufferAgent = listBufferAgent[0]
    
    # Create and add this part creator to the cyber context
    partCreatora = PartCreatorforBuffer(startingBuffer,startingBufferPosition,exitHumanAgent, startTime, partCreatingInterval)

    #print(partCreatora.getProductAgent().productHistory.vertices)
   
    print('environmentModel')
    for i, vertice in enumerate(partCreatora.getProductAgent().environmentModel.vertices):
        print(i,vertice.getProcessCompleted())

    print('productHistory')
    for i, vertice in enumerate(partCreatora.getProductAgent().productHistory.vertices):
        print(i,vertice.getProcessCompleted())

    #print('bid')
    #for i, vertice in enumerate(partCreatora.getProductAgent().productHistory.vertices):
    #    print(i,vertice.getProcessCompleted())



    productHistory=partCreatora.getProductAgent().productHistory
    environmentModel=partCreatora.getProductAgent().environmentModel
    #print(partCreatora.getProductAgent().getProduct().getPart().getPartName())




    return machineX,machineY,robotX,robotY,listMachineAgent,listBufferAgent,listRobotAgent,productHistory,environmentModel


