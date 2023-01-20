try:
    from utils import *
    from name_collector import Context, MapInfo, FunctionInfo
except:
    from utils07.assembly import DIR
    from utils08.utils import *
    from utils08.name_collector import Context, MapInfo, FunctionInfo

def way(pos1, pos2): 
        return (abs(pos1[0]-pos2[0]) * [(DIR.N if pos1[0]-pos2[0] > 0 else DIR.S)]) + (abs(pos1[1]-pos2[1]) * [(DIR.W if pos1[1]-pos2[1] > 0 else DIR.E)])

print(way((0,0), (2,3)))

directions = {
    DIR.N: 'N',
    DIR.E: 'E',
    DIR.S: 'S',
    DIR.W: 'W'
}

def gen_move(pos1, pos2):
    code = ''
    for dir in way(pos1, pos2):
        code+=f"mov {directions[dir]};\n"
    return code

class CodeGenerator(object):
    '''
    Generador de Codigo
    '''
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context):        
        context = Context()
        for defx in node.defs:
            self.visit(defx, context)
        if 'MAIN' not in context.functions.keys():
            self.errors.append('No existe ninguna funcion de inicio: "MAIN".') 
        elif len(context.functions['MAIN'].args) > 0:
            count = len(context.functions['MAIN'].args)
            self.errors.append(f'La funcion de inicio: "MAIN" debe tener 0 argumentos y esta definida con {count}.') 
        return self.errors, context

    ####################################################

    @visitor.when(PlusNode)
    def visit(self, node, context:Context):
        pos0 = node.left.tup
        pos1 = node.center.tup
        pos2 = node.right.tup

        context.code+= gen_move(context.current_position, pos1)
        context.code+= 'copy;\n'
        context.code+= gen_move(pos1, pos2)
        context.code+= 'add;\n'
        context.code+= gen_move(pos2, pos0)
        context.code+= 'paste;\n'
        context.current_position = pos0

    @visitor.when(MinusNode)
    def visit(self, node, context:Context):
        pos0 = node.left.tup
        pos1 = node.center.tup
        pos2 = node.right.tup

        context.code+= gen_move(context.current_position, pos1)
        context.code+= 'copy;\n'
        context.code+= gen_move(pos1, pos2)
        context.code+= 'sub;\n'
        context.code+= gen_move(pos2, pos0)
        context.code+= 'paste;\n'
        context.current_position = pos0

    @visitor.when(StarNode)
    def visit(self, node, context:Context):
        pos0 = node.left.tup
        pos1 = node.center.tup
        pos2 = node.right.tup

        context.code+= gen_move(context.current_position, pos1)
        context.code+= 'copy;\n'
        context.code+= gen_move(pos1, pos2)
        context.code+= 'mul;\n'
        context.code+= gen_move(pos2, pos0)
        context.code+= 'paste;\n'
        context.current_position = pos0

    @visitor.when(DivNode)
    def visit(self, node, context:Context):
        pos0 = node.left.tup
        pos1 = node.center.tup
        pos2 = node.right.tup

        context.code+= gen_move(context.current_position, pos1)
        context.code+= 'copy;\n'
        context.code+= gen_move(pos1, pos2)
        context.code+= 'add;\n'
        context.code+= gen_move(pos2, pos0)
        context.code+= 'div;\n'
        context.current_position = pos0

    @visitor.when(IncNode)
    def visit(self, node, context:Context):
        pos0 = node.lex.tup        

        context.code+= gen_move(context.current_position, pos0)
        context.code+= 'inc;\n'
        context.current_position = pos0

    @visitor.when(DecNode)
    def visit(self, node, context:Context):
        pos0 = node.lex.tup        

        context.code+= gen_move(context.current_position, pos0)
        context.code+= 'dec;\n'
        context.current_position = pos0

    #############################################

    @visitor.when(PrintNode)
    def visit(self, node, context:Context):
        context.code+= 'print;\n'

    #############################################

    @visitor.when(IfEndNode)
    def visit(self, node, context: Context):
        preview_pos = context.current_position
        
