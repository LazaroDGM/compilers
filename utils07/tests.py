from time import sleep
from assembly import Robot, map, DIR


# class Agent:
#     def __init__(self):
#         self.stack = []
#     def func(self, args):
#         self.stack.append(4)

# class Action:
#     def __init__(self) -> None:
#         self.stack = []
#     def Add(self, func, args):
#         self.stack.append((func, args))



# agent = Agent()
# action = Action()

# action.Add(agent.func, [])
# action.stack[-1][0](action.stack[-1][1])

# print(agent.stack)









################# Test 2 #################



# mapp = map((10, 10))
# robot = Robot(mapp)


# robot.move(DIR.S)
# robot.move(DIR.S)
# robot.move(DIR.S)
# robot.move(DIR.S)
# robot.move(DIR.S)
# print(robot.position)

# robot.move(DIR.E)
# robot.move(DIR.E)
# robot.move(DIR.E)
# robot.move(DIR.E)
# robot.move(DIR.E)
# print(robot.position)

# robot.move(DIR.N)
# robot.move(DIR.N)
# robot.move(DIR.N)
# robot.move(DIR.N)
# robot.move(DIR.N)
# print(robot.position)

# robot.move(DIR.W)
# robot.move(DIR.W)
# robot.move(DIR.W)
# robot.move(DIR.W)
# robot.move(DIR.W)
# print(robot.position)



################# Test 3 #################

# mapp = map((5, 5))
# robot = Robot(mapp)

# print(mapp.pipes)

# print(mapp.pipes)
# mapp.addPipe((1, 1), (0, 0))
# mapp.addHamper((0, 0))
# print(mapp.pipes)

# mapp.push(8, (0, 0))
# mapp.push(9, (0, 0))
# mapp.push(4, (0, 0))
# mapp[0, 0] =  0
# mapp[1, 1] =  1


# item = mapp.field_values[0][0]
# item = mapp.field_values[0][0]

# print(item)


################# Test 4 #################

# class A:
#     def __init__(self) -> None:
#         self.a, self.b = (4, 3)

# a = A()
# print(a.a, a.b)

################# Test 5 #################
# mapp = map(dimension=(5, 5))
# robot = Robot()

# robot.enqueue_instruction(robot.move, [DIR.S])
# robot.enqueue_instruction(robot.move, [DIR.S])
# robot.enqueue_instruction(robot.move, [DIR.S])
# robot.enqueue_instruction(robot.move, [DIR.S])
# robot.enqueue_instruction(robot.move, [DIR.S])

# robot.enqueue_instruction(robot.move, [DIR.N])
# robot.enqueue_instruction(robot.move, [DIR.N])
# robot.enqueue_instruction(robot.move, [DIR.N])
# robot.enqueue_instruction(robot.move, [DIR.N])
# robot.enqueue_instruction(robot.move, [DIR.N])

# robot.enqueue_instruction(robot.GoTo, [0])

# for instruction in robot.instructions:
#     sleep(1)
#     print(f"Se ha realizado la instruccion: {instruction}")


################# Test 6 #################

# mapp.addPipe((0, 0), (4, 4))
# for i in range(mapp.getLength[0]):
#     for j in range(mapp.getLength[1]):
#         mapp[i, j] = 1

# for i in range(mapp.getLength[0]):
#     for j in range(mapp.getLength[1]):
#         mapp.push(1, (i, j))
        
# robot.enqueue_instruction(robot.cut, [])

# for ins in robot.instructions:
#     print(end="")
# print(mapp.field_values)
# print(robot.hand_box)


################# Test 7 #################
# map1 = map(dimension=(6, 6))
# map1.addHamper((0, 0))
# map1.push(2, (0, 0))

# robot.enqueue_instruction(robot.overlap, [map1])
# robot.enqueue_instruction(robot.copy, [])
# robot.enqueue_instruction(robot.add, [])
# robot.enqueue_instruction(robot.paste_push, [])

# robot.enqueue_instruction(robot.overlap, [map1])                           # Instruccion 4
# robot.enqueue_instruction(robot.copy, [])
# robot.enqueue_instruction(robot.add, [])
# robot.enqueue_instruction(robot.paste_push, [])                           # Instruccion 7

# robot.enqueue_instruction(robot.cut, [])
# robot.enqueue_instruction(robot.paste, [])
# robot.enqueue_instruction(robot.paste_push, [])
# robot.enqueue_instruction(robot.printHandBox, [])                           # Instruccion 11

# robot.enqueue_instruction(robot.copy, [])                                       # Instruccion 12
# robot.enqueue_instruction(robot.move, [DIR.E])                                       # Instruccion 13
# robot.enqueue_instruction(robot.paste, [])

# robot.enqueue_instruction(robot.move, [DIR.W])                          # Instruccion 15
# robot.enqueue_instruction(robot.copy, [])                                       # Instruccion 16
# robot.enqueue_instruction(robot.move, [DIR.E])                                       # Instruccion 17
# robot.enqueue_instruction(robot.decrem, [])                                       # Instruccion 18
# robot.enqueue_instruction(robot.copy, [])                                       # Instruccion 19

# robot.enqueue_instruction(robot.printHandBox, [])                           # Instruccion 20

# robot.enqueue_instruction(robot.GoToIfPositive, [15])                           # Instruccion 21

# for inst in robot.instructions:
#     sleep(1)
#     print(inst)


# print(robot.map[0, 0])
# print(robot.map.field_values[0][0])


################# Test 8 #################


# mapp = map(dimension=(3, 4))
# mapp[0, 0] = 0
# mapp[1, 0] = 5
# mapp[1, 1] = 2
# robot = Robot()

# robot.enqueue_instruction(robot.overlap, [mapp])
# robot.enqueue_instruction(robot.move, [DIR.S])
# robot.enqueue_instruction(robot.copy, [])
# robot.enqueue_instruction(robot.decrem, [])
# robot.enqueue_instruction(robot.GoToIfZero, [14])                   # 5

# robot.enqueue_instruction(robot.move, [DIR.E])                      # 6
# robot.enqueue_instruction(robot.copy, [])
# robot.enqueue_instruction(robot.add, [])
# robot.enqueue_instruction(robot.paste, [])

# robot.enqueue_instruction(robot.move, [DIR.W])                  # 10
# robot.enqueue_instruction(robot.GoTo, [2])

# robot.enqueue_instruction(robot.copy, [])                               # 12
# robot.enqueue_instruction(robot.add, [])
# robot.enqueue_instruction(robot.copy, [])

# robot.enqueue_instruction(robot.move, [DIR.E])                      # 15
# robot.enqueue_instruction(robot.copy, [])
# robot.enqueue_instruction(robot.printHandBox, [])

# for i in robot.instructions:
#     print(i)


################# Test 9 - Fibonacci #################

# mapp = map(dimension=(2, 2))
# mapp[0, 0] = 1
# mapp[0, 1] = 1
# mapp[1, 1] = 40
# robot = Robot()

# robot.enqueue_instruction(robot.overlap, [mapp])              # 0
# robot.enqueue_instruction(robot.copy, [])                           # 1
# robot.enqueue_instruction(robot.move, [DIR.E])                # 2
# robot.enqueue_instruction(robot.add, [])                            # 3
# robot.enqueue_instruction(robot.paste, [])                          # 4  
# robot.enqueue_instruction(robot.move, [DIR.S])                # 5
# robot.enqueue_instruction(robot.sub, [])                             # 6
# robot.enqueue_instruction(robot.GoToIfNegative, [9])        # 7

# robot.enqueue_instruction(robot.GoTo, [15])                      # 8

# robot.enqueue_instruction(robot.move, [DIR.N])                # 9
# robot.enqueue_instruction(robot.copy, [])                          # 10
# robot.enqueue_instruction(robot.move, [DIR.W])              # 11
# robot.enqueue_instruction(robot.sub, [])                            # 12
# robot.enqueue_instruction(robot.paste, [])                          # 13
# robot.enqueue_instruction(robot.GoTo, [2])                           # 14

# robot.enqueue_instruction(robot.move, [DIR.N])                # 15
# robot.enqueue_instruction(robot.copy, [])                            # 16
# robot.enqueue_instruction(robot.printHandBox, [])             # 17

# for i in robot.instructions:
#     a = i

################# Test 9 - Fibonacci con Memoria #################

# mapp = map(dimension=(2, 2))
# mapp.addPipe((0, 0), (1, 0))
# mapp[0, 0] = 1
# mapp.push(1, (1, 0))
# mapp[0, 1] = 40
# robot = Robot()

# robot.enqueue_instruction(robot.overlap, [mapp])            # 0
# robot.enqueue_instruction(robot.cut, [])                            # 1
# robot.enqueue_instruction(robot.add, [])                            # 2
# robot.enqueue_instruction(robot.move, [DIR.E])              # 3
# robot.enqueue_instruction(robot.sub, [])                           # 4
# robot.enqueue_instruction(robot.GoToIfPositive, [13])      # 5

# robot.enqueue_instruction(robot.add, [])                            # 6

# robot.enqueue_instruction(robot.move, [DIR.W])              # 7

# robot.enqueue_instruction(robot.paste_push, [])              # 8
# robot.enqueue_instruction(robot.move, [DIR.S])              # 9
# robot.enqueue_instruction(robot.cut, [])                           # 10
# robot.enqueue_instruction(robot.move, [DIR.N])             # 11
# robot.enqueue_instruction(robot.GoTo, [2])                     # 12

# robot.enqueue_instruction(robot.add, [])                          # 13
# robot.enqueue_instruction(robot.printHandBox, [])          # 14

# for i in robot.instructions:
#     a = i

################# Test 10 - Potencia Recursiva #################

mapp = map(dimension=(2, 2))
mapp[0, 0] = 4
mapp[0, 1] = 3
robot = Robot()

robot.enqueue_instruction(robot.overlap, [mapp])                                                    # 0
robot.enqueue_instruction(robot.move, [DIR.E])                                                       # 1
robot.enqueue_instruction(robot.decrem, [])                                                             # 2
robot.enqueue_instruction(robot.copy, [])                                                                  # 3
robot.enqueue_instruction(robot.GoToIfZero, [11])                                                   # 4
robot.enqueue_instruction(robot.push_mem, [])                                                       # 5
robot.enqueue_instruction(robot.overlap, [])                                                            # 6
robot.enqueue_instruction(robot.enqueue_instruction, [robot.pull, []])                     # 7
robot.enqueue_instruction(robot.enqueue_instruction, [robot.move, [DIR.W]])       # 8
robot.enqueue_instruction(robot.enqueue_instruction, [robot.mul, []])                    # 9
robot.enqueue_instruction(robot.GoTo, [1])                                                             # 10
robot.enqueue_instruction(robot.enqueue_instruction, [robot.printHandBox, []])    # 11


for i in robot.instructions:
    a = 1