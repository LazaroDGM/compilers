try:
    from utils import *
    from type_collector import Context, MapInfo, LabelInfo
    from assembly import Robot, Map, Action, DIR
except:
    from utils07.utils import *
    from utils07.type_collector import Context, MapInfo, LabelInfo
    from utils07.assembly import Robot, Map, Action, DIR

directions = {
    'N': DIR.N,
    'S': DIR.S,
    'E': DIR.E,
    'W': DIR.W
}


class CodeGenerator(object):
    '''
    Generador de Codigo
    '''    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context: Context):
        context.code += \
'''
import numpy as np
from collections import deque
import enum


'''
        self.visit(node.sec_maps, context)                
        self.visit(node.sec_inst, context)        
        return context

    ####################################################      

    @visitor.when(SecMapsNode)
    def visit(self, node: SecMapsNode, context: Context):
        context.code+=\
'''
###### MAPS ######


'''        
        for mapx in node.maps:
            self.visit(mapx, context)        

    @visitor.when(SecInstructionNode)
    def visit(self, node: SecInstructionNode, context: Context):
        context.code+= \
'''
###### INST #######

context.robot = Robot()


'''    
        context.current_index = 0
        node.instructions.append(NopNode())
        for inst in node.instructions:
            self.visit(inst, context)

    ##################### .MAPS ########################

    @visitor.when(MapDeclaration)
    def visit(self, node: SecMapsNode, context: Context):
        m = Map((len(node.map), len(node.map[0])))


        context.code += \
f'''
##### {node.id} ######
{node.id} = Map(({len(node.map)}, {len(node.map[0])}))

'''
        for i, row in enumerate(node.map):
            for j, col in enumerate(row):
                self.visit(node.map[i][j], context, node.id, i, j)
        context.code+='\n'
        return m

    @visitor.when(SquareNode)
    def visit(self, node: SquareNode, context: Context, map_name: str, i, j):
        if node.lex == 'V':
            pass
        elif node.lex == 'H':            
            context.code+= f'{map_name}.addHamper(({i},{j}))\n'
        else:
            ######TODO#######
            # Incluir Pipes #
            #################
            num = int(node.lex)
            context.code += f'{map_name}[{i},{j}] = {num}\n'
            

    #################################################    

    @visitor.when(MovNode)
    def visit(self, node: MovNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.move, [DIR.{node.lex}])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    #---------GOTOs-------------#

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.GoTo, [{context.labels[node.lex].index_instr}])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(GotoIfZeroNode)
    def visit(self, node: GotoIfZeroNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.GoToIfZero, [{context.labels[node.lex].index_instr}])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1


    @visitor.when(GotoIfPositive)
    def visit(self, node: GotoIfPositive, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.GoToIfPositive, [{context.labels[node.lex].index_instr}])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(GotoIfNegative)
    def visit(self, node: GotoIfNegative, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.GoToIfNegative, [{context.labels[node.lex].index_instr}])'        
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    #------------------------#

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode, context: Context):
        context.code += f'#### {node.lex} ####\n' 

    @visitor.when(OverlapNode)
    def visit(self, node: OverlapNode, context: Context):
        robot = context.robot
        robot : Robot
        code  = f'robot.enqueue_instruction(robot.overlap, [ {node.lex} ])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(PullNode)
    def visit(self, node: PullNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.pull, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(PushNode)
    def visit(self, node: PushNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.paste_push, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(PopNode)
    def visit(self, node: PopNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.cut, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.copy, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1
    
    @visitor.when(PasteNode)
    def visit(self, node: PasteNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.paste, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    #----------Aritmetics------------#

    @visitor.when(AddNode)
    def visit(self, node: AddNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.add, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(SubNode)
    def visit(self, node: SubNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.sub, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(DivNode)
    def visit(self, node: DivNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.div, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(MulNode)
    def visit(self, node: MulNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.mul, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    #@visitor.when(ModNode)
    #def visit(self, node: ModNode, context: Context):
    #    robot = context.robot
    #    robot : Robot
    #    robot.enqueue_instruction(robot.)

    @visitor.when(DecNode)
    def visit(self, node: DecNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.decrem, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(IncNode)
    def visit(self, node: IncNode, context: Context):
        robot = context.robot
        robot : Robot
        code  = f'robot.enqueue_instruction(robot.increm, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    #---------------------------------#

    @visitor.when(PushMemNode)
    def visit(self, node: PushMemNode, context: Context):
        robot = context.robot
        robot : Robot
        code = 'robot.enqueue_instruction(robot.push_mem, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(PopMemNode)
    def visit(self, node: PopMemNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.pop_mem, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(NopNode)
    def visit(self, node: NopNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.none, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, context: Context):
        robot = context.robot
        robot : Robot
        code = f'robot.enqueue_instruction(robot.printHandBox, [])'
        context.code += code + f'   # {context.current_index}\n'
        context.current_index += 1

    