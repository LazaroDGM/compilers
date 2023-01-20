try:
    from utils import *
    from name_collector import Context, MapInfo, FunctionInfo
except:
    from utils08.utils import *
    from utils08.name_collector import Context, MapInfo, FunctionInfo

class SemanticCheck(object):
    '''
    Chequeo Semantico
    '''
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context: Context):        
        for defx in node.defs:
            self.visit(defx, context) 
        for name_map in context.unused_maps():
            self.warnings.append(f"El mapa {name_map} ha sido definido pero nunca usado")
        for name_label in context.unused_functions():
            self.warnings.append(f"La funcion {name_label} ha sido definida pero nunca usada")
        return self.errors, self.warnings, context

    ####################################################

    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, context: Context):
        if not context.is_map_defined(node.id_map):
            self.errors.append(f"El mapa {node.id_map} no esta definido")
        else:
            context.maps_invocation[node.id_map] = True
        for inst in node.instructions:
            self.visit(inst, context)


    @visitor.when(CallFunctionNode)
    def visit(self, node: CallFunctionNode, context: Context):
        if not context.is_function_defined(node.id):
            self.errors.append(f"La funcion {node.id} no esta definida")
        else:
            context.functions_invocation[node.id] = True
            if len(node.tuple_list) != len(context.functions[node.id].args):
                self.errors.append(f"La funcion {node.id} debe recibir {len(context.functions[node.id].args)} y esta recibiendo {len(node.tuple_list)} argumentos")


    @visitor.when(IfEndNode)
    def visit(self, node, context:Context):
        for inst in node.instructions_if:
            self.visit(inst, context)

    @visitor.when(IfElseEndNode)
    def visit(self, node, context:Context):
        for inst in node.instructions_if:
            self.visit(inst, context)
        for inst in node.instructions_else:
            self.visit(inst, context)

    @visitor.when(WhileNode)
    def visit(self, node, context:Context):
        for inst in node.instructions_while:
            self.visit(inst, context)