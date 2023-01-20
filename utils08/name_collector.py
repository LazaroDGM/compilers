try:
    from utils import *
except:
    from utils08.utils import *


class MapInfo:
    def __init__(self, id) -> None:
        self.id = id

class FunctionInfo:
    def __init__(self, id, id_map, args) -> None:
        self.id = id
        self.id_map = id_map
        self.args = args
        

class Context:
    def __init__(self):
        self.maps = {}
        self.maps_invocation = {}          

        self.code = ''

        self.functions = {}
        self.functions_invocation = {}        

        self.current_position= (0,0)


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

    def define_function(self, name, name_map, args):
        if self.get_function_info(name) is None and self.get_map_info(name) is None:
            label_info = FunctionInfo(name, name_map, args)
            self.functions[name] = label_info
            self.functions_invocation[name] = False
            return True
        return False

    def is_function_defined(self, name):
        return name in self.functions.keys()

    def get_function_info(self, name):
        return self.functions.get(name, None)

    def unused_functions(self):
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
        if 'MAIN' not in context.functions.keys():
            self.errors.append('No existe ninguna funcion de inicio: "MAIN".') 
        elif len(context.functions['MAIN'].args) > 0:
            count = len(context.functions['MAIN'].args)
            self.errors.append(f'La funcion de inicio: "MAIN" debe tener 0 argumentos y esta definida con {count}.') 
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
            context.define_function(node.id_func, node.id_map, node.reserving)