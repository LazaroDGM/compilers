try:
    from utils import *
except:
    from utils07.utils import *

class LabelInfo:
    def __init__(self, idx, index) -> None:
        self.id = idx
        self.index_instr = index

class Context:
    def __init__(self):
        self.labels = {}
        self.labels_invocation = {}
        self.current_index = 0

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
    Recolector de Nombre de Mapas y Etiquetas de salto
    '''
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context=None):        
        context = Context()
        #self.visit(self.sec_maps, context)
        self.visit(node.sec_inst, context)
        return self.errors

    @visitor.when(SecMapsNode)
    def visit(self, node: SecMapsNode, context: Context):
        pass

    @visitor.when(SecInstructionNode)
    def visit(self, node: SecInstructionNode, context: Context):
        for inst in node.instructions:
            if isinstance(inst, LabelNode):
                self.visit(inst, context)
            else:
                context.inc_index()

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode, context: Context):
        if not context.define_label(node.lex):
            self.errors.append(f"La etiqueta de {node.lex} ya esta definida")
    
