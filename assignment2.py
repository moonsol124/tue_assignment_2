# assignment 2

from asyncio import create_subprocess_shell
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

def searchTileSameColumn(robot):
    object = robot.scan_object_ahead().upper()
    if (object == "TILE"):
        steps = robot.scan_steps_ahead()
        goForward(robot, steps+1)
        return True
    return False

def script_3(robot): # Where is the Tile
    # your solution here:
    # the robot finds the tile and ends up on top of the tile.
    # the robot does not crash into a wall
    # make the robot facing downwards
    
    # check if the tile is in the same column.
    # check downwards first.
    makeTheRobotFacingDown(robot)
    if (searchTileSameColumn(robot)):
        print ("found!")
        return
    
    # check upwards.
    makeTheRobotFacingUp(robot)
    if (searchTileSameColumn(robot)):
        print ("found!")
        return

    # keep searching for the tile.
    # scan downwards
    makeTheRobotFacingDown(robot)
    stepsToBottom = robot.scan_steps_ahead()
    firstHalfResult = searchTile(robot, stepsToBottom)
    if (firstHalfResult == True):
        return
    
    # scan upwards
    turnRight(robot, 2)
    stepsToTop = robot.scan_steps_ahead()
    secondHalfResult = searchTile(robot, stepsToTop, False)
    
    if (secondHalfResult == True):
        print ("found!")
        return
            
    return # end of script_3


def script_4(robot):  # Walk around the Block
    # your solution here:

    return # end of script_4


def script_5(robot):  # Follow the Tile Path
    # your solution here:

    return # end of script_5


def script_6(robot):  # Push the Block over the Tile
    # your solution here:

    return # end of script_6
