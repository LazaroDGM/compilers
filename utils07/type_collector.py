try:
    from utils import *
except:
    from utils07.utils import *


class MapInfo:
    def __init__(self, idx) -> None:
        self.id = idx

class LabelInfo:
    def __init__(self, idx, index) -> None:
        self.id = idx
        self.index_instr = index

class Context:
    def __init__(self):
        self.maps = {}

        self.labels = {}
        self.labels_invocation = {}
        self.current_index = 0


    ###################### MAPS ########################

    def define_map(self, name):
        if self.get_map_info(name) is None:
            map_info = MapInfo(name)
            self.maps[name] = map_info
            return True
        return False

    def is_map_defined(self, name):
        return name in self.maps.keys()

    def get_map_info(self, name):
        return self.maps.get(name, None)


    ###################### INST ########################
    def inc_index(self):
        self.current_index += 1

    def define_label(self, name):
        if self.get_label_info(name) is None:
            label_info = LabelInfo(name, self.current_index)
            self.labels[name] = label_info
            self.labels_invocation[name] = False
            return True
        return False

    def is_label_defined(self, name):
        return name in self.labels.keys()

    def get_label_info(self, name):
        return self.labels.get(name, None)

    


class TypeCollector(object):
    '''
    Recolector de Nombres de Mapas y Etiquetas de salto
    '''
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context=None):        
        context = Context()
        self.visit(node.sec_maps, context)
        self.visit(node.sec_inst, context)
        return self.errors, context

    ####################################################

    @visitor.when(SecMapsNode)
    def visit(self, node: SecMapsNode, context: Context):
        for mapx in node.maps:
            self.visit(mapx, context)        

    @visitor.when(SecInstructionNode)
    def visit(self, node: SecInstructionNode, context: Context):
        for inst in node.instructions:
            if isinstance(inst, LabelNode):
                self.visit(inst, context)
            else:
                context.inc_index()

    ###################################################

    ###################### MAPS #######################

    @visitor.when(MapDeclaration)
    def visit(self, node: MapDeclaration, context: Context):
        if not context.define_map(node.id):
            self.errors.append(f"El mapa {node.id} ya esta definido")

        assert len(node.map) > 0, 'Mapa sin Filas'
        assert len(node.map[0]) > 0, 'Mapa con Fila sin Columnas'

        count_cols = len(node.map[0])
        for row in node.map:
            if len(row) != count_cols:
                self.errors.append(f"Mapa {node.id} con filas de distinto tamanno")
                break

    ###################### INST #######################

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode, context: Context):
        if not context.define_label(node.lex):
            self.errors.append(f"La etiqueta de {node.lex} ya esta definida")
    
