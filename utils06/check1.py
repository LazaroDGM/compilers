try:
    from utils import *
except:
    from utils06.utils import *

defined_types = [
    'bool',
    'int'
]

class VariableInfo:
    def __init__(self, name, ttype):
        self.name = name
        self.type = ttype

class ConstInfo:
    def __init__(self, name, ttype):
        self.name = name
        self.type = ttype

class FunctionInfo:
    def __init__(self, name, params, types):
        self.name = name
        self.params = params
        self.types = types

class Scope:
    def __init__(self, parent=None):
        self.local_vars = []
        self.local_consts = []
        self.local_funcs = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname, ttype):
        if not self.is_local_var(vname):
            vinfo = VariableInfo(vname, ttype)
            self.local_vars.append(vinfo)
            return True
        return False

    def define_const(self, cname, ttype):
        if not self.is_local_const(cname):
            cinfo = ConstInfo(cname, ttype)
            self.local_consts.append(cinfo)
            return True
        return False
    
    def define_function(self, fname, params, types):        
        if not self.is_local_func(fname):
            finfo = FunctionInfo(fname, params, types)
            self.local_funcs.append(finfo)
            return True
        return False

    def is_var_defined(self, vname):        
        child = self
        while child is not None:            
            vinfo = self.get_local_variable_info(vname)
            if vinfo is not None:
                return True
            child = self.parent
        return False

    def is_const_defined(self, cname):        
        child = self
        while child is not None:            
            cinfo = self.get_local_const_info(cname)
            if cinfo is not None:
                return True
            child = self.parent
        return False
    
    def is_func_defined(self, fname, n):        
        child = self
        while child is not None:            
            finfo = self.get_local_function_info(fname, n)
            if finfo is not None:
                return True
            child = self.parent
        return False


    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None

    def is_local_const(self, vname):
        return self.get_local_const_info(vname) is not None
    
    def is_local_func(self, fname):
        return self.get_local_function_info(fname) is not None

    def get_local_variable_info(self, vname):
        for vinfo in self.local_vars:
            if vinfo.name == vname:
                return vinfo     
        return None

    def get_local_const_info(self, cname):
        for cinfo in self.local_consts:
            if cinfo.name == cname:
                return cinfo     
        return None
    
    def get_local_function_info(self, fname):
        for finfo in self.local_funcs:
            if finfo.name == fname:
                return finfo     
        return None

class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):        
        scope = Scope()
        for st in node.statements:
            st : StatementNode
            self.visit(st, scope)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):  
        if node.ttype not in defined_types:
            self.errors.append(f"El tipo '{node.ttype}' de la variable '{node.id}' no esta definido.")
        if scope.is_local_const(node.id):
            self.errors.append(f"Existe una constante '{node.id}' ya definida previamente.")
        if not scope.define_variable(vname= node.id,ttype=node.ttype):
            self.errors.append(f"La variable '{node.id}' ya ha sido definida previamente.")
        self.visit(node.expr, scope)

    @visitor.when(ConstDeclarationNode)
    def visit(self, node: ConstDeclarationNode, scope: Scope):
        if node.ttype not in defined_types:
            self.errors.append(f"El tipo '{node.ttype}' de la constante '{node.id}' no esta definido.")
        if scope.is_local_var(node.id):
            self.errors.append(f"Existe una variable '{node.id}' ya definida previamente.")
        if not scope.define_const(vname= node.id,ttype=node.ttype):
            self.errors.append(f"La constante '{node.id}' ya ha sido definida previamente.")
        self.visit(node.expr, scope)
        
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):  
        if not scope.define_function(node.id, params= node.params, types= node.types):
            self.errors.append(f"La funcion '{node.id}' ya esta definida.")        
        child = scope.create_child_scope()
        for nparam, tparam in zip(node.params, node.types):
            if tparam not in defined_types:
                self.errors.append(f"El tipo '{tparam}' del parametro '{nparam}' no esta definido.")
            if not child.define_variable(nparam, tparam):
                self.errors.append(f"El parametro '{nparam}' ya esta definido")
        self.visit(node.body, child)

###########################################################  
    
    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):        
        try:
            value = float(node.lex)
            node.lex = value
        except:
            self.errors.append('No se puede convertir a float')
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):        
        if not scope.is_var_defined(node.lex):
            self.errors.append(f'La variable {node.lex} no ha sido definida.')          
    
    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):        
        if not scope.is_func_defined(node.lex, len(node.args)):
            self.errors.append(f'La funcion {node.lex} no ha sido definida')        
        for arg in node.args:
            arg: ExpressionNode
            self.visit(arg, scope)    
    
    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope: Scope):        
        self.visit(node.left, scope)
        self.visit(node.right, scope) 