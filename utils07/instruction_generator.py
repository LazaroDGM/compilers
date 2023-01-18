try:
    from utils import *
    from type_collector import Context, MapInfo, LabelInfo
    from assembly import Robot, Map, Action
except:
    from utils07.utils import *
    from utils07.type_collector import Context, MapInfo, LabelInfo
    from utils07.assembly import Robot, Map, Action


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
    def visit(self, node: ProgramNode):
        reals_maps = self.visit(node.sec_maps)
        print('Hola')

    ####################################################      

    @visitor.when(SecMapsNode)
    def visit(self, node: SecMapsNode):
        maps = {}
        for mapx in node.maps:
            m = self.visit(mapx)
            maps[mapx.id] = m
        return maps

    ###################################################

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

