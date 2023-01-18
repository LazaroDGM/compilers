try:
    from utils import *
    from type_collector import Context, MapInfo, LabelInfo
except:
    from utils07.utils import *
    from utils07.type_collector import Context, MapInfo, LabelInfo

class SemanticCheck(object):
    '''
    Chequeo de reglas semanticas
    '''    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context: Context):        
        self.visit(node.sec_inst, context)
        for name_map in context.unused_maps():
            self.warnings.append(f"El mapa {name_map} ha sido definido pero nunca usado")
        for name_label in context.unused_labels():
            self.warnings.append(f"La etiqueta {name_label} ha sido definida pero nunca usada")
        return self.errors, self.warnings, context

    ####################################################      

    @visitor.when(SecInstructionNode)
    def visit(self, node: SecInstructionNode, context: Context):
        for inst in node.instructions:
            if isinstance(inst, GotoGeneric):
                self.visit(inst, context)
            elif isinstance(inst, OverlapNode):
                self.visit(inst, context)

    ###################################################

    ###################### INST #######################

    @visitor.when(GotoGeneric)
    def visit(self, node: GotoGeneric, context: Context):
        if not context.is_label_defined(node.lex):
            self.errors.append(f"La etiqueta {node.lex} no esta definida")
        else:
            context.labels_invocation[node.lex] = True

    @visitor.when(OverlapNode)
    def visit(self, node: OverlapNode, context: Context):
        if not context.is_map_defined(node.lex):
            self.errors.append(f"El mapa {node.lex} no esta definido")
        else:
            context.maps_invocation[node.lex] = True
            