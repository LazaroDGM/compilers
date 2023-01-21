
import numpy as np
from collections import deque
import enum
from utils07.assembly import Map, Robot, DIR



###### MAPS ######

##### M1 ######
M1 = Map((3, 4))

M1[2,1] = 190
M1.addHamper((2,3))


##### M2 ######
M2 = Map((3, 4))

M2[0,0] = 0
M2[1,0] = 5
M2[1,1] = 2


###### INST #######

robot = Robot()


robot.enqueue_instruction(robot.move, [DIR.S])   # 0
robot.enqueue_instruction(robot.move, [DIR.S])   # 1
robot.enqueue_instruction(robot.move, [DIR.E])   # 2
robot.enqueue_instruction(robot.move, [DIR.E])   # 3
robot.enqueue_instruction(robot.move, [DIR.E])   # 4
robot.enqueue_instruction(robot.move, [DIR.N])   # 5
robot.enqueue_instruction(robot.move, [DIR.W])   # 6
robot.enqueue_instruction(robot.move, [DIR.W])   # 7
robot.enqueue_instruction(robot.move, [DIR.N])   # 8
robot.enqueue_instruction(robot.move, [DIR.W])   # 9
robot.enqueue_instruction(robot.move, [DIR.S])   # 10
#### PorGusto ####
#### WHILE ####
robot.enqueue_instruction(robot.copy, [])   # 11
robot.enqueue_instruction(robot.decrem, [])   # 12
robot.enqueue_instruction(robot.GoToIfZero, [22])   # 13
robot.enqueue_instruction(robot.move, [DIR.E])   # 14
robot.enqueue_instruction(robot.copy, [])   # 15
robot.enqueue_instruction(robot.add, [])   # 16
robot.enqueue_instruction(robot.paste, [])   # 17
robot.enqueue_instruction(robot.move, [DIR.W])   # 18
robot.enqueue_instruction(robot.GoTo, [11])   # 19
robot.enqueue_instruction(robot.printHandBox, [])   # 20
robot.enqueue_instruction(robot.printHandBox, [])   # 21
#### ENDWHILE ####
robot.enqueue_instruction(robot.move, [DIR.E])   # 22
robot.enqueue_instruction(robot.copy, [])   # 23
robot.enqueue_instruction(robot.printHandBox, [])   # 24
robot.enqueue_instruction(robot.none, [])   # 25

try:
    for inst in robot.instructions:
        pass
except Exception as e:
    print('Error en tiempo de Ejecucion en :')
    print(e)
