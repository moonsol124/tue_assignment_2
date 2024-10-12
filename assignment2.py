# assignment 2

from asyncio import create_subprocess_shell

from flair import set_proxies
from numpy import block
from robot_world import *

def show_duo_names():
    print()
    print('┌─────────────────────┬───────────────────────┐')
    print('│ 0HV120 assignment 2 │ Robot World           │')
    print('├─────────────────────┼───────────────────────┤')
    print('│ duo partner 1       │ name 1                │')
    print('├─────────────────────┼───────────────────────┤')
    print('│ duo partner 2       │ name 2                │')
    print('└─────────────────────┴───────────────────────┘')


def script_0_demo(robot):
    # demo script to show the capabilities of the robot
    # read the assignment instructions for details

    # demo of scans
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of stepping and turning
    for _ in range(3):
        robot.step_forward()
    robot.turn_left()
    robot.turn_right()
    robot.turn_right()
    for _ in range(4):
        robot.step_forward()
    for _ in range(4):
        robot.step_back()
    robot.turn_left()
    robot.step_back()
    robot.step_back()
    robot.turn_right()

    # demo of scans
    print()
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of grabbing, pushing forward, dragging backward and releasing of a block
    robot.step_forward() # when the robot faces and touches the block it can grab it
    robot.grab_release_block()

    # moving the block
    for _ in range(5):
        robot.step_forward()
    for _ in range(3):
        robot.step_back()

    robot.grab_release_block()  # releasing the block

    robot.step_back()
    robot.turn_right()
    robot.turn_right()
    robot.turn_right()
    for _ in range(3): # finally, crash robot into the wall
        robot.step_back()

    return # end of demo

################################################
#   helper functions defined by you can go here:
#   start of helper function part



#   end of helper function part
################################################

def goForward(robot, steps):
    for step in range(steps):
        robot.step_forward()


def checkIfDistanceIsEqual(distances):
    if (len(distances) == 0):
        return True
    if (distances.count(distances[0]) == len(distances)):
        return True
    return False

def turnLeft(robot, steps):
    for step in range(steps):
        robot.turn_left()

def turnRight(robot, steps):
    for step in range(steps):
        robot.turn_right()

def searchRoom(robot, steps, goDown=True):
    if (goDown==False):
        steps = steps + 1

    index = 0
    left = []
    right = []

    for step in range(steps):
        index += 1
        turnLeft(robot, 1)
        left.append(robot.scan_steps_ahead())
        turnRight(robot, 2)
        right.append(robot.scan_steps_ahead())
        turnLeft(robot, 1)
        if (step != steps):
            goForward(robot, 1)

    leftSide = checkIfDistanceIsEqual(left)
    rightSide = checkIfDistanceIsEqual(right)

    distance = 0
    maxValue = 0
    if (leftSide == False):
        distance = left.index(max(left))
        maxValue = max(left)
    if (rightSide == False):
        distance = right.index(max(right))
        maxValue = max(right)  
    if (leftSide == False or rightSide == False):
        turnRight(robot, 2)
        if (goDown == True):
            goForward(robot, index-distance)
        if (goDown == False):
            goForward(robot, (index-distance)-1)
        if (leftSide == False):
            turnRight(robot, 1)
        if (rightSide == False):
            turnLeft(robot, 1)
        goForward(robot, maxValue)
        return True
    return False

def makeTheRobotFacingDown(robot):
    direction = robot.scan_direction()
    if (direction == "RIGHT"):
        robot.turn_right()
    if (direction == "UP"):
        for step in range(2):
            robot.turn_right()
    if (direction == "LEFT"):
        robot.turn_left()

def makeTheRobotFacingUp(robot):
    direction = robot.scan_direction()
    if (direction == "RIGHT"):
        robot.turn_left()
    if (direction == "DOWN"):
        for step in range(2):
            robot.turn_left()
    if (direction == "right"):
        robot.turn_left()

def makeTheRobotFacingRight(robot):
    direction = robot.scan_direction()
    if (direction == "UP"):
        robot.turn_right()
    if (direction == "DOWN"):
        robot.turn_left()
    if (direction == "LEFT"):
        turnLeft(robot, 2)

def makeTheRobotFacingLeft(robot):
    direction = robot.scan_direction()
    if (direction == "UP"):
        robot.turn_left()
    if (direction == "DOWN"):
        robot.turn_right()
    if (direction == "RIGHT"):
        turnRight(robot, 2)


def script_1(robot):   # Walk around the World
    # your solution here:
    # the robot first goes to one of the corners.
    # •the robot next walks around the World along the outer wall and stops in the corner where it started.
    # •the robot does not crash into a wall

    # direction = robot.scan_direction()
    # obstacle = robot.scan_object_ahead()
    # steps = robot.scan_steps_ahead()
    # energy = robot.scan_energy()
    # print (direction, obstacle, steps, energy)
    WALLS = 4
    # make the robot facing down
    makeTheRobotFacingDown(robot)

    # go down
    firstSteps = robot.scan_steps_ahead()
    goForward(robot, firstSteps)

    # go to the left bottom, this is our starting corner.
    robot.turn_right()
    secondSteps = robot.scan_steps_ahead()
    goForward(robot, secondSteps)

    # TO DO: later on, you can improve it by choosing to select the coner with shortest distance at the bottom.

    sum = 0
    for wall in range(0, WALLS):
        robot.turn_right()
        curForwardSteps = robot.scan_steps_ahead()
        goForward(robot, curForwardSteps)
        sum += curForwardSteps+1
    print ("Total steps to walk around the world: ", sum)

    # check the distance between the wall and the robot.
    # movie that much distance to the wall.
    # then either turn left or right.
    return # end of script_1

def script_2(robot):  # Switch Rooms
    # your solution here:
    # the robot walks from the room where it was created to the other room.
    # the robot has to stop moving/turning in the other room (the exact location is not important).
    # the robot does not crash into a wall
    # sometimes it happens that there is no open tile to the other room.


    # make the robot facing downwards
    makeTheRobotFacingDown(robot)

    # scan the first half
    stepsToBottom = robot.scan_steps_ahead()
    firstHalfResult = searchRoom(robot, stepsToBottom)
    if (firstHalfResult == True):
        print ("found!")
        return
    
    # scan the second half
    turnRight(robot, 2)
    stepsToTop = robot.scan_steps_ahead()
    secondHalfResult = searchRoom(robot, stepsToTop)

    if (secondHalfResult == True):
        print ("found!")
        return
            
    print ("there is no open tile to the other room!")
    return # end of script_2

def goToTile(robot, object):
    if (object=="TILE"):
        distance = robot.scan_steps_ahead()
        goForward(robot, distance+1)
        return True
    
    return False

def searchTile(robot, steps, goDown=True):
    if (goDown==False):
        steps = steps + 1

    index = 0
    for step in range(steps):
        index += 1
        turnLeft(robot, 1)
        isFound = goToTile(robot, robot.scan_object_ahead().upper())
        if (isFound):
            return True
        else:
            turnRight(robot, 2)
            isFound = goToTile(robot, robot.scan_object_ahead().upper())
            if (isFound):
                return True
            else:
                turnLeft(robot, 1)
                if (step != steps):
                    goForward(robot, 1)

def searchTileCurColumn(robot, object):
    object = object.upper()
    if (object == "TILE"):
        steps = robot.scan_steps_ahead()
        goForward(robot, steps+1)
        return True
    return False

def checkWallFourDirections(robot):
    # avoid wall along same x-axis
    objects = []
    makeTheRobotFacingUp(robot)
    objects.append(robot.scan_object_ahead().upper())
    makeTheRobotFacingRight(robot)
    objects.append(robot.scan_object_ahead().upper())
    makeTheRobotFacingDown(robot)
    objects.append(robot.scan_object_ahead().upper())
    makeTheRobotFacingLeft(robot)
    objects.append(robot.scan_object_ahead().upper())

    # check if all items are the same
    return objects, objects.count(objects[0]) == len(objects)    

def calculateCurCoordinates(robot):
    makeTheRobotFacingLeft(robot)
    distanceLeft = robot.scan_steps_ahead() + 1
    makeTheRobotFacingDown(robot)
    distanceDown = robot.scan_steps_ahead() + 1
    return distanceLeft, distanceDown

def serachAndgoToTheTile(robot):
    # check downwards first.
    makeTheRobotFacingDown(robot)
    object = robot.scan_object_ahead()
    isFound = searchTileCurColumn(robot, object)
    if (isFound):
        print ("found!")
        return calculateCurCoordinates(robot)
    
    # check upwards.
    makeTheRobotFacingUp(robot)
    object = robot.scan_object_ahead()
    isFound = searchTileCurColumn(robot, object)
    if (isFound):
        print ("found!")
        return calculateCurCoordinates(robot)

    # keep searching for the tile.
    # scan downwards
    makeTheRobotFacingDown(robot)
    stepsToBottom = robot.scan_steps_ahead()
    firstHalfResult = searchTile(robot, stepsToBottom)
    if (firstHalfResult == True):
        print ("found!")
        return calculateCurCoordinates(robot)
    
    # scan upwards
    turnRight(robot, 2)
    stepsToTop = robot.scan_steps_ahead()
    secondHalfResult = searchTile(robot, stepsToTop, False)
    
    if (secondHalfResult == True):
        print ("found!")
        return calculateCurCoordinates(robot)

    return False

def script_3(robot): # Where is the Tile
    x, y = serachAndgoToTheTile(robot)
    print (f"coordinates of the tile is ({x}, {y})")
    return # end of script_3


def goToBlock(robot, object):
    if (object=="BLOCK"):
        distance = robot.scan_steps_ahead()
        goForward(robot, distance)
        return True
    
    return False

def searchBlock(robot, steps, goDown=True):
    if (goDown==False):
        steps = steps + 1

    index = 0
    for step in range(steps):
        index += 1
        turnLeft(robot, 1)
        isFound = goToBlock(robot, robot.scan_object_ahead().upper())
        if (isFound):
            return True
        else:
            turnRight(robot, 2)
            isFound = goToBlock(robot, robot.scan_object_ahead().upper())
            if (isFound):
                return True
            else:
                turnLeft(robot, 1)
                if (step != steps):
                    goForward(robot, 1)

def searchTileSameColumn(robot):
    object = robot.scan_object_ahead().upper()
    if (object == "BLOCK"):
        steps = robot.scan_steps_ahead()
        goForward(robot, steps)
        return True
    return False

def script_4(robot):  # Walk around the Block
    # the robot first walks to the blue block until they touch.
    # •the robot then walks around the block in clock-wise direction (while
    # touching the block) completing exactly one full round.
    # •the robot does not crash into a wall or the block
    # your solution here:
    
    # check where the block is.. from up, down, right, left sides?
    # same as searching for a tile...
    # but then you have to check the direction of the robot.    

    blockFound = False
    # check if there is a block in the same column.
    # check downwards.
    if (blockFound == False):
        makeTheRobotFacingDown(robot)
        if (searchTileSameColumn(robot)):
            blockFound = True
    # check upwards.
    if (blockFound == False):
        makeTheRobotFacingUp(robot)
        if (searchTileSameColumn(robot)):
            blockFound = True
    # keep searching for the block.
    # scan downwards
    if (blockFound == False):
        makeTheRobotFacingDown(robot)
        stepsToBottom = robot.scan_steps_ahead()
        firstHalfResult = searchBlock(robot, stepsToBottom)
        if (firstHalfResult == True):
            blockFound = True
    # scan upwards   
    if (blockFound == False):
        turnRight(robot, 2)
        stepsToTop = robot.scan_steps_ahead()
        secondHalfResult = searchBlock(robot, stepsToTop, False)
        if (secondHalfResult == True):
            blockFound = True

    direction = robot.scan_direction()
    maxWalkDistance = 8
    # now walk around the block
    # the robot faces the block from left, right, top, bottom
    for step in range(maxWalkDistance):
        if (step == 0):
            turnLeft(robot, 1)
            goForward(robot, 1)
        elif (step%2 == 1 and step != maxWalkDistance-1):
            turnRight(robot, 1)
            goForward(robot, 2)
        elif (step == maxWalkDistance-1):
            turnRight(robot, 1)
            goForward(robot, 1)

    return # end of script_4

def isTile(robot):
    object = robot.scan_object_ahead().upper()
    steps = robot.scan_steps_ahead()
    if (object == "TILE" and steps < 1):
        return True
    return False

def isOppositeDirection(originalDirection, curDirection):
        if (originalDirection == "RIGHT"):
            if (curDirection == "LEFT"):
                return True
        
        if (originalDirection == "LEFT"):
            if (curDirection == "RIGHT"):
                return True
            
        if (originalDirection == "UP"):
            if (curDirection == "DOWN"):
                return True
            
        if (originalDirection == "DOWN"):
            if (curDirection == "UP"):
                return True

def findPath(robot, originalDirection):
    for i in range(4):
        if (i < 3):
            turnRight(robot, 1)
            curDirection = robot.scan_direction()
            checkOpps = isOppositeDirection(originalDirection, curDirection)
            if (checkOpps):
                pass
            else:
                if (isTile(robot)):
                    return True
        else:
            print ("the end of the path!")
            return False

def script_5(robot):  # Follow the Tile Path
    makeTheRobotFacingRight(robot)
    
    while(True):        
        if (isTile(robot)):
            print (robot.scan_steps_ahead())
            goForward(robot, 1)
        else:
            originalDirection = robot.scan_direction()
            if (findPath(robot, originalDirection) == False):
                break
            
    return # end of script_5

def checkIfthereIsWay(robot):
    distance = robot.scan_steps_ahead()
    if (distance > 0):
        return True
    return False

def goOneStepEitherToLeftOrRight(robot):
    makeTheRobotFacingRight(robot)
    if (checkIfthereIsWay(robot)):
        goForward(robot, 1)
    else:
        makeTheRobotFacingLeft(robot)
        goForward(robot, 1)

def goOneStepEitherUpOrDown(robot):
    makeTheRobotFacingUp(robot)
    if (checkIfthereIsWay(robot)):
        goForward(robot, 1)
    else:
        makeTheRobotFacingDown(robot)
        goForward(robot, 1)

def avoidBlock(robot):
    objects, isAllWall = checkWallFourDirections(robot)
    makeTheRobotFacingDown(robot)
    index = 0
    if (isAllWall == False):
        index = objects.index("BLOCK")
        if (index == 0 or index == 2):
            goOneStepEitherToLeftOrRight(robot)
        else:
            goOneStepEitherUpOrDown(robot)

def findBlock(robot, steps, goDown=True):
    if (goDown==False):
        steps = steps + 1

    index = 0
    for step in range(steps):
        index += 1
        turnLeft(robot, 1)
        isFound = goToBlock(robot, robot.scan_object_ahead().upper())
        if (isFound):
            return True
        else:
            turnRight(robot, 2)
            isFound = goToBlock(robot, robot.scan_object_ahead().upper())
            if (isFound):
                return True
            else:
                turnLeft(robot, 1)
                if (step != steps):
                    goForward(robot, 1)

def goToBlockScript_6(robot):
    blockFound = False
    # check if there is a block in the same column.
    # check downwards.
    if (blockFound == False):
        makeTheRobotFacingDown(robot)
        if (searchTileSameColumn(robot)):
            blockFound = True
    # check upwards.
    if (blockFound == False):
        makeTheRobotFacingUp(robot)
        if (searchTileSameColumn(robot)):
            blockFound = True
    # keep searching for the block.
    # scan downwards
    if (blockFound == False):
        makeTheRobotFacingDown(robot)
        stepsToBottom = robot.scan_steps_ahead()
        firstHalfResult = findBlock(robot, stepsToBottom)
        if (firstHalfResult == True):
            blockFound = True
    # scan upwards   
    if (blockFound == False):
        turnRight(robot, 2)
        stepsToTop = robot.scan_steps_ahead()
        secondHalfResult = findBlock(robot, stepsToTop, False)
        if (secondHalfResult == True):
            blockFound = True

def isFacingBlockFromRightDirection(robot, direction):
    curDirection = robot.scan_direction()
    turnRight(robot, 1)
    isBlock = robot.scan_object_ahead().upper()
    if (isBlock == "BLOCK" and direction == curDirection):
        return True
    turnLeft(robot, 1)
    return False


def putRobotInRightDirection(robot, direction):
    maxWalkDistance = 8
    for step in range(maxWalkDistance):
        if (step == 0):
            turnLeft(robot, 1)
            goForward(robot, 1)
            if (isFacingBlockFromRightDirection(robot, direction)):
                break
        elif (step%2 == 1 and step != maxWalkDistance-1):
            turnRight(robot, 1)
            goForward(robot, 2)
            if (isFacingBlockFromRightDirection(robot, direction)):
                    break
        elif (step == maxWalkDistance-1):
            turnRight(robot, 1)
            goForward(robot, 1)
            if (isFacingBlockFromRightDirection(robot, direction)):
                break
        
def script_6(robot):  # Push the Block over the Tile
    # your solution here:
    makeTheRobotFacingDown(robot)
    isTileFound = serachAndgoToTheTile(robot)
    if (isTileFound == False):
        makeTheRobotFacingDown(robot)
        goToBlockScript_6(robot)
        # then perform actions to drag the block...

    direction = robot.scan_direction()
    if (direction == "LEFT"):
        goOneStepEitherUpOrDown(robot)
        makeTheRobotFacingLeft(robot)
        goForward(robot, 2)
    if (direction == "RIGHT"):
        goOneStepEitherUpOrDown(robot)
        makeTheRobotFacingRight(robot)
        goForward(robot, 2)

    # perform another search..
    makeTheRobotFacingDown(robot)
    isTileFound = serachAndgoToTheTile(robot)

    makeTheRobotFacingUp(robot)
    distance = robot.scan_steps_ahead()
    tileX = 0
    tileY = 0
    if (distance > 0):
        goForward(robot, 1)
        tileX, tileY = calculateCurCoordinates(robot)
        tileY -= 1
        makeTheRobotFacingDown(robot)
        goForward(robot, 1)
    else:
        makeTheRobotFacingDown(robot)
        goForward(robot, 1)
        tileX, tileY = calculateCurCoordinates(robot)
        tileY += 1
        makeTheRobotFacingUp(robot)
        goForward(robot, 1)
    print (tileX, tileY)

    # find the block...
    goToBlockScript_6(robot)
    robotDirectionFacingBlock = robot.scan_direction()
    robotX = 0
    robotY = 0
    
    makeTheRobotFacingUp(robot)
    distance = robot.scan_steps_ahead()
    if (distance > 0):
        goForward(robot, 1)
        robotX, robotY = calculateCurCoordinates(robot)
        robotY -= 1
        makeTheRobotFacingDown(robot)
        goForward(robot, 1)
        if (robotDirectionFacingBlock == "RIGHT"):
            makeTheRobotFacingRight(robot)
        else:
            makeTheRobotFacingLeft(robot)
    else:
        makeTheRobotFacingDown(robot)
        goForward(robot, 1)
        robotX, robotY = calculateCurCoordinates(robot)
        robotY += 1
        makeTheRobotFacingUp(robot)
        goForward(robot, 1)
        if (robotDirectionFacingBlock == "RIGHT"):
            makeTheRobotFacingRight(robot)
        else:
            makeTheRobotFacingLeft(robot)

    blockX = robotX
    blockY = robotY
    if (robotDirectionFacingBlock == 'RIGHT'):
        blockX += 1
    if (robotDirectionFacingBlock == 'LEFT'):
        blockX -= 1
    if (robotDirectionFacingBlock == 'UP'):
        blockY += 1
    if (robotDirectionFacingBlock == 'DOWN'):
        blockY -= 1
    print (blockX, blockY)    

    # x axis first
    # if (tileX < blockX):

    #     putRobotInRightDirection(robot, )

    #     # put the robot to the left of the block.
    # if (tileX > blockX):
        # put the robot the right of the block
    # robot.grab_release_block()
    # goForward(robot, 1)
    # robot.step_back()
    # robot.step_back()
    # robot.step_back()

    # there is always a tile
    # if you can't find a block then move horizontally to find it

    # with block you can move only forward and backward
    # you have to change the position of the block by walking around
    return # end of script_6
