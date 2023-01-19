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


class InstructionGenerator(object):
    '''
    Generador de Instrucciones
    '''    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context: Context):
        self.visit(node.sec_maps, context)                
        self.visit(node.sec_inst, context= context)
        return context

    ####################################################      

    @visitor.when(SecMapsNode)
    def visit(self, node: SecMapsNode, context: Context):
        maps = {}
        for mapx in node.maps:
            m = self.visit(mapx)
            maps[mapx.id] = m
        context.reals_maps = maps        

    @visitor.when(SecInstructionNode)
    def visit(self, node: SecInstructionNode, context: Context):
        context.robot = Robot()
        for inst in node.instructions:
            self.visit(inst, context)

    ##################### .MAPS ########################

    @visitor.when(MapDeclaration)
    def visit(self, node: SecMapsNode):
        m = Map((len(node.map), len(node.map[0])))
        for i, row in enumerate(node.map):
            for j, col in enumerate(row):
                self.visit(node.map[i][j], m, i, j)
        return m

    @visitor.when(SquareNode)
    def visit(self, node: SquareNode, map: Map, i, j):
        if node.lex == 'V':
            pass
        elif node.lex == 'H':
            map.addHamper((i,j))            
        else:
            ######TODO#######
            # Incluir Pipes #
            #################
            num = int(node.lex)
            map[i,j]= num

    #################################################    

    @visitor.when(MovNode)
    def visit(self, node: MovNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.move, [directions[node.lex]])

    #---------GOTOs-------------#

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.GoTo, [context.labels[node.lex].index_instr])

    @visitor.when(GotoIfZeroNode)
    def visit(self, node: GotoIfZeroNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.GoToIfZero, [context.labels[node.lex].index_instr])

    @visitor.when(GotoIfPositive)
    def visit(self, node: GotoIfPositive, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.GoToIfPositive, [context.labels[node.lex].index_instr])

    @visitor.when(GotoIfNegative)
    def visit(self, node: GotoIfNegative, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.GoToIfNegative, [context.labels[node.lex].index_instr])

    #------------------------#

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode, context: Context):
        pass

    @visitor.when(OverlapNode)
    def visit(self, node: OverlapNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.overlap, [context.reals_maps[node.lex]])

    @visitor.when(PullNode)
    def visit(self, node: PullNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.pull, [])

    @visitor.when(PushNode)
    def visit(self, node: PushNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.paste_push, [])

    @visitor.when(PopNode)
    def visit(self, node: PopNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.cut, [])

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.copy, [])
    
    @visitor.when(PasteNode)
    def visit(self, node: PasteNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.paste, [])

    #----------Aritmetics------------#

    @visitor.when(AddNode)
    def visit(self, node: AddNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.add, [])

    @visitor.when(SubNode)
    def visit(self, node: SubNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.sub, [])

    @visitor.when(DivNode)
    def visit(self, node: DivNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.div, [])

    @visitor.when(MulNode)
    def visit(self, node: MulNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.mul, [])

    #@visitor.when(ModNode)
    #def visit(self, node: ModNode, context: Context):
    #    robot = context.robot
    #    robot : Robot
    #    robot.enqueue_instruction(robot.)

    @visitor.when(DecNode)
    def visit(self, node: DecNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.decrem, [])

    @visitor.when(IncNode)
    def visit(self, node: IncNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.increm, [])

    #---------------------------------#

    @visitor.when(PushMemNode)
    def visit(self, node: PushMemNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.push_mem, [])

    @visitor.when(PopMemNode)
    def visit(self, node: PopMemNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.pop_mem, [])

    @visitor.when(NopNode)
    def visit(self, node: NopNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.none, [])

    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, context: Context):
        robot = context.robot
        robot : Robot
        robot.enqueue_instruction(robot.printHandBox, [])

    