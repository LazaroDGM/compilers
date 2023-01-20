try:
    from utils import *
except:
    from utils08.utils import *


class MapInfo:
    def __init__(self, idx) -> None:
        self.id = idx

class FunctionInfo:
    def __init__(self, idx) -> None:
        self.id = idx
        

class Context:
    def __init__(self):
        self.maps = {}
        self.maps_invocation = {}          

        self.code = ''

        self.functions = {}
        self.functions_invocation = {}        


    ###################### MAPS ########################

    def define_map(self, name):
        if self.get_map_info(name) is None and self.get_function_info(name) is None:
            map_info = MapInfo(name)
            self.maps[name] = map_info
            self.maps_invocation[name] = False
            return True
        return False

    def is_map_defined(self, name):
        return name in self.maps.keys()

    def get_map_info(self, name):
        return self.maps.get(name, None)

    def unused_maps(self):
        return list(
            filter(
                lambda name: not self.maps_invocation[name], self.maps.keys()
                )
            )


    ###################### INST ########################

    def define_function(self, name):
        if self.get_function_info(name) is None and self.get_map_info(name) is None:
            label_info = FunctionInfo(name)
            self.functions[name] = label_info
            self.functions_invocation[name] = False
            return True
        return False

    def is_function_defined(self, name):
        return name in self.functions.keys()

    def get_function_info(self, name):
        return self.functions.get(name, None)

    def unused_labels(self):
        return list(
            filter(
                lambda name: not self.functions_invocation[name], self.functions.keys()
                )
            )
    


class NameCollector(object):
    '''
    Recolector de Nombres de Mapas y Funciones
    '''
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, context):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, context=None):        
        context = Context()
        for defx in node.defs:
            self.visit(defx, context)
        if 'main' not in context.functions.keys():
            self.errors.append('No existe ninguna funcion de inicio: "main".')        
        return self.errors, context

    ####################################################

    @visitor.when(MapDefinitionNode)
    def visit(self, node: MapDefinitionNode, context: Context):
        if context.is_map_defined(node.id):
            self.errors.append(f'Ya existe un mapa definido con el mismo nombre: "{node.id}"')
        elif context.is_function_defined(node.id):
            self.errors.append(f'Ya existe una funcion definida con el mismo nombre: "{node.id}"')
        else:
            context.define_map(node.id)

    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, context: Context):
        if context.is_map_defined(node.id_func):
            self.errors.append(f'Ya existe un mapa definido con el mismo nombre: "{node.id_func}"')
        elif context.is_function_defined(node.id_func):
            self.errors.append(f'Ya existe una funcion definida con el mismo nombre: "{node.id_func}"')
        else:
            context.define_function(node.id_func)    