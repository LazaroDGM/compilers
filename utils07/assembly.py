import numpy as np
from collections import deque
import enum


class DIR(enum.Enum):
    N = 0 # north
    S = 1 # south
    E = 2 # east
    W = 3 # west
class CELL(enum.Enum):
    V = 0 # void
    H = 1 # hamper
    P = 2 # pipe
    D = 3 # digit

class Map:
    def __init__(self, dimension) -> None:
        self.field_types = np.full(dimension, CELL.V)
        self.field_values = np.full(dimension, None)
        self.pipes = {}
        self.getLength = dimension
    def __getitem__(self, key):
        """ Retorna el elemento de la posicion "key". En caso que en esa posicion haya un hamper o tuberia, devuelve el elemento del tope sin retirarlo"""
        try:
            if self.field_types[key[0]][key[1]] == CELL.H:
                try:
                    peek = self.field_values[key[0]][key[1]].pop()
                    self.field_values[key[0]][key[1]].append(peek)
                    return peek
                except: raise Exception(f"No existian elementos en el hamper ubicado en {key}")
            elif self.field_types[key[0]][key[1]] == CELL.P:
                try:
                    right_tale_pipe = self.pipes[key][0]
                    peek = self.field_values[key[0]][key[1]].pop() if right_tale_pipe else self.field_values[key[0]][key[1]].popleft()
                    self.field_values[key[0]][key[1]].append(peek)
                    return peek
                except: raise Exception(f"No existian elementos en el pipe ubicado en {key}")
            else: return self.field_values[key[0]][key[1]]
        except Exception as e:
            raise Exception(f"__getitem__(): error al indexar con la llave {key}, -> {e}")
    def __setitem__(self, key, new_value):
        """ Pone un elemento en la posicion "key". En caso de haber un hamper, pone en el tope de dicho hamper el elemento a insertar, en caso de haber elementos en el hamper, sustituyendo el tope, 
        en caso contrario le hace push y lo pone en el tope como unico elemento """
        try:
            if self.field_types[key[0]][key[1]] == CELL.H:
                try: self.field_values[key[0]][key[1]].pop()
                except: pass
                self.field_values[key[0]][key[1]].append(new_value)
            elif self.field_types[key[0]][key[1]] == CELL.P:
                right_tale_pipe = self.pipes[key][0]
                try: 
                    self.field_values[key[0]][key[1]].pop() if right_tale_pipe else self.field_values[key[0]][key[1]].popleft()
                except: pass
                self.field_values[key[0]][key[1]].append(new_value) if right_tale_pipe else self.field_values[key[0]][key[1]].appendleft(new_value)
            else: 
                self.field_values[key[0]][key[1]] = new_value
                self.field_types[key[0]][key[1]] = CELL.D
        except:
            raise Exception(f"__setitem__(): error al indexar con la llave {key}")

    def push(self, value, key):
        """ Le hace push al valor a introducir en caso de haber un hamper, en otro caso sobrescribe el valor que hay en "key" """
        try:
            if self.field_types[key[0]][key[1]] == CELL.H:
                self.field_values[key[0]][key[1]].append(value)
            elif self.field_types[key[0]][key[1]] == CELL.P:
                right_tale_pipe = self.pipes[key][0]
                self.field_values[key[0]][key[1]].append(value) if right_tale_pipe else self.field_values[key[0]][key[1]].appendleft(value)
            else:
                self.field_values[key[0]][key[1]] = value
                self.field_types[key[0]][key[1]] = CELL.D
        except:
            raise Exception(f"push(): error al indexar con la llave: {key}")
    def pop(self, key):
        """ Le hace pop al hamper en la posicion "key", en caso que no haya hamper, vacia el elemento  """
        try:
            if self.field_types[key[0]][key[1]] == CELL.H:
                try:
                    return self.field_values[key[0]][key[1]].pop()
                except: raise Exception(f"pop(): el hamper en {key} no tiene elementos para devolver")
            elif self.field_types[key[0]][key[1]] == CELL.P:
                try:
                    right_tale_pipe = self.pipes[key][0]
                    return self.field_values[key[0]][key[1]].pop() if right_tale_pipe else self.field_values[key[0]][key[1]].popleft()
                except: raise Exception(f"pop(): el hamper en {key} no tiene elementos para devolver")
            else:
                peek = self.field_values[key[0]][key[1]]
                self.field_values[key[0]][key[1]] = None
                self.field_types[key[0]][key[1]] = CELL.V
                return peek
        except Exception as e:
            raise Exception(f"pop(): error al indexar con la llave: {key} -> {e}")

    def addHamper(self, position):
        """ Funcion que agrega un Hamper (pila) en position"""
        try:
            if position[0] not in range(0, self.getLength[0]) or position[1] not in range(0, self.getLength[1]):
                raise Exception(f"addHamper(): posicion {position} fuera de rango")
        except:
            raise Exception(f"addHamper(): posicion \"{position}\" invalida")
        self.field_types[position[0]][position[1]] = CELL.H
        self.field_values[position[0]][position[1]] = deque()
    def addPipe(self, pos1, pos2):
        """ Funcion que agrega un Pipe (tuberia o doble cola) en position. Si en el diccionario "pipes" tiene como primer elemento correspondiente al valor que tiene como llave su posicion,
         un True, es la punta derecha de la doble cola o "deque". En caso contrario, o sea, que tenga False, es el extremo izquierdo de la doble cola
        """
        try:
            if pos1[0] not in range(0, self.getLength[0]) or pos1[1] not in range(0, self.getLength[1]) or pos2[0] not in range(0, self.getLength[0]) or pos2[1] not in range(0, self.getLength[1]):
                raise Exception("addPipe(): posicion fuera de rango")
        except:
            raise Exception("addPipe(): posicion invalida")
        self.field_types[pos1[0]][pos1[1]] = CELL.P
        self.field_types[pos2[0]][pos2[1]] = CELL.P

        self.pipes[pos1] = (True, pos2)
        self.pipes[pos2] = (False, pos1)
        
        self.field_values[pos1[0]][pos1[1]] = deque()
        self.field_values[pos2[0]][pos2[1]] = self.field_values[pos1[0]][pos1[1]]
    
        

            
        
class Robot:
    def __init__(self) -> None:
        self.position = (-1, -1)
        self.hand_box = None
        self.map = None

        self.instructions = InstructionStack()
        self.maps_stack = deque()
        self.memo_stack = deque()

    ### Copy Paste ###        
    def copy(self):
        self.hand_box = self.map[self.position]
    def cut(self):
        self.hand_box = self.map.pop(self.position)
    def paste(self):
        self.map[self.position] = self.hand_box
    def paste_push(self):
        self.map.push(self.hand_box, self.position)
        self.drop_hand()
    def drop_hand(self):
        self.hand_box = None
    def none(self):
        pass


    ### Aritmetica ###
    def add(self):
        if self.empty_hands(): raise Exception("add(): manos vacias")
        self.hand_box += self.map[self.position]
    def sub(self):
        if self.empty_hands(): raise Exception("sub(): manos vacias")
        self.hand_box -= self.map[self.position]
    def mul(self):
        if self.empty_hands(): raise Exception("mul(): manos vacias")
        self.hand_box *= self.map[self.position]
    def div(self):
        if self.empty_hands(): raise Exception("div(): manos vacias")
        self.hand_box //= self.map[self.position]
    def increm(self):
        self.map[self.position] += 1
    def decrem(self):
        self.map[self.position] -= 1
        self.copy()
    def empty_hands(self): return self.hand_box is None
    

    ### Prints ###
    def printHandBox(self): print(f"hand box: {self.hand_box}")
    
    
    ### Memoria ###
    def push_mem(self):
        """ Toma lo que tiene el Robot en las manos y los pushea a la memoria. No se elimina lo que se tiene en las manos por comididad para algunas operaciones"""
        if self.hand_box is None:
            raise Exception("push_mem(): manos vacias")
        self.memo_stack.append(self.hand_box)
    def pop_mem(self):
        """ Toma lo que esta en el tope de la memoria y lo lleva a sus manos """
        try: self.hand_box = self.memo_stack.pop()
        except: raise Exception("pop_mem(): Memoria vacia")
    
    ### Move ###
    def move(self, dir:DIR):
        if dir == DIR.N:
            self.position = (self.position[0] - 1, self.position[1])
        if dir == DIR.S:
            self.position = (self.position[0] + 1, self.position[1])
        if dir == DIR.W:
            self.position = (self.position[0], self.position[1] - 1)
        if dir == DIR.E:
            self.position = (self.position[0], self.position[1] + 1)
        # Aqui se podria controlar si la nueva posicion es correcta


    ### Recursividad ###
    def overlap(self, mapp:Map = None):
        """ Toma el mapa actual y lo almacena en la pila en forma de tupla junto a la actual posicion. Luego asigna al robot los nuevos mapa y posicion como sus actuales """
        if self.map != None: self.maps_stack.append((self.map, self.position))
    
        if mapp == None:
            mapp = self.map
    
        new_mapp = Map(dimension=(mapp.getLength[0], mapp.getLength[1]))
        for i in range(new_mapp.getLength[0]):
            for j in range(new_mapp.getLength[0]):
                new_mapp.field_types[i][j] = mapp.field_types[i][j]
                if mapp.field_types[i][j] == CELL.H:
                    new_mapp.field_values[i][j] = mapp.field_values[i][j].copy()
                elif mapp.field_types[i][j] == CELL.P:
                    if (i, j) in new_mapp.pipes: continue

                    right_tale_pipe_flag = mapp.pipes[(i, j)][0]
                    other_tale_position = mapp.pipes[(i, j)][1]
                    
                    new_mapp.field_values[i][j] = mapp.field_values[i][j].copy()                            # Crea una copia de la tuberia
                    new_mapp.field_values[other_tale_position[0]][other_tale_position[1]] = new_mapp.field_values[i][j]

                    new_mapp.pipes[(i, j)] = (right_tale_pipe_flag, other_tale_position)                # Agregamos ambas, cola derecha e izquierda de la pila a "pipes" y no visitamos de nuevo dichas posiciones
                    new_mapp.pipes[other_tale_position] = (not right_tale_pipe_flag, (i, j))

                else: new_mapp.field_values[i][j] = mapp.field_values[i][j]
        
        self.map, self.position = new_mapp, (0, 0)

    def pull(self):
        """Lo contrario del overlap: saca el viejo mapa y la vieja posicion y los reemplaza por los actuales, desechando estos ultimos"""
        try: self.map, self.position = self.maps_stack.pop()
        except: raise Exception("pull(): no habian mapas en la pila")
            
    
    def enqueue_instruction(self, func, params):
        self.instructions.add(func, params)


    ### Saltos de instruccion ###
    def GoTo(self, index):
        if index not in range(0, len(self.instructions.instructions)): raise Exception("GoTo(): no esta en rango el indice de salto")
        self.instructions.indicator = index
    def GoToIfPositive(self, index):
        if self.hand_box > 0: 
            if index not in range(0, len(self.instructions.instructions)):
                raise Exception(f"GoToPositive(): indice {index} fuera de rango")
            self.instructions.indicator = index
    def GoToIfNegative(self, index):
        if self.hand_box < 0: 
            if index not in range(0, len(self.instructions.instructions)):
                raise Exception(f"GoToPositive(): indice {index} fuera de rango")
            self.instructions.indicator = index
    def GoToIfZero(self, index):
        if self.hand_box == 0: 
            if index not in range(0, len(self.instructions.instructions)):
                raise Exception(f"GoToPositive(): indice {index} fuera de rango")
            self.instructions.indicator = index


class Action:
    """ Clase para agrupar una funcion y parametros para invocarla """
    def __init__(self, function, params):
        self.__dict__.update(func=function, args=params)
class InstructionStack:
    """ Clase disennada para iterarla como forma de recorrer sus instrucciones internas """
    def __init__(self) -> None:
        self.indicator = 0
        self.instructions: list(Action) = []
    def add(self, func, args):
        self.instructions.append(Action(function=func, params=args))
    def __iter__(self):
        while True:
            if self.indicator >= len(self.instructions): 
                self.indicator = 0
                return
            yield f"{self.instructions[self.indicator].func}( {self.instructions[self.indicator].args} )"

            temp_indicator = self.indicator
            self.instructions[self.indicator].func(*(self.instructions[self.indicator].args))                   # Invocando la funcion
            indicator_jump_flag = temp_indicator != self.indicator                                                  # Comprobacion de, si fue una instruccion de salto 

            if not indicator_jump_flag: self.indicator = temp_indicator + 1

    
            
