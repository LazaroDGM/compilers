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
    def __init__(self, name, params: ParamListNode):
        self.name = name
        self.params = params

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
    
    def define_function(self, fname, params):        
        if not self.is_local_func(fname):
            finfo = FunctionInfo(fname, params)
            self.local_funcs.append(finfo)
            return True
        return False

    def is_var_defined(self, vname):        
        child = self
        while child is not None:            
            vinfo = self.get_local_variable_info(vname)
            if vinfo is not None:
                return True
            child = child.parent
        return False

    def is_const_defined(self, cname):        
        child = self
        while child is not None:            
            cinfo = self.get_local_const_info(cname)
            if cinfo is not None:
                return True
            child = child.parent
        return False
    
    def is_func_defined(self, fname):        
        child = self
        while child is not None:            
            finfo = self.get_local_function_info(fname)
            if finfo is not None:
                return True
            child = child.parent
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
        elif not scope.define_variable(vname= node.id,ttype=node.ttype):
            self.errors.append(f"La variable '{node.id}' ya ha sido definida previamente.")
        self.visit(node.expr, scope)

    @visitor.when(AsignVarNode)
    def visit(self, node: AsignVarNode, scope: Scope):        
        if scope.is_local_const(node.id):
            self.errors.append(f"Existe una constante '{node.id}' ya definida previamente.")
        elif not scope.is_local_var(vname= node.id):
            self.errors.append(f"No existe ninguna variable '{node.id}'.")
        self.visit(node.expr, scope)

    @visitor.when(ConstDeclarationNode)
    def visit(self, node: ConstDeclarationNode, scope: Scope):
        if node.ttype not in defined_types:
            self.errors.append(f"El tipo '{node.ttype}' de la constante '{node.id}' no esta definido.")
        elif scope.is_local_var(node.id):
            self.errosrs.append(f"Existe una variable '{node.id}' ya definida previamente.")
        if not scope.define_const(cname= node.id,ttype=node.ttype):
            self.errors.append(f"La constante '{node.id}' ya ha sido definida previamente.")
        self.visit(node.expr, scope)
        
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):  
        if not scope.define_function(node.id, params= node.params):
            self.errors.append(f"La funcion '{node.id}' ya esta definida.")        
        child = scope.create_child_scope()
        self.visit(node.params, child)
        for st in node.body:                        
            self.visit(st, child)

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode, scope: Scope):
        self.visit(node.expr, scope)

###########################################################

    @visitor.when(ParamListNode)
    def visit(self, node: ParamListNode, scope: Scope):
        for param in node.params:
            self.visit(param, scope)
    
    @visitor.when(ParamNode)
    def visit(self, node: ParamNode, scope: Scope):
        nparam, tparam = node.id, node.ttype
        if tparam not in defined_types:
            self.errors.append(f"El tipo '{tparam}' del parametro '{nparam}' no esta definido.")
        if not scope.define_variable(nparam, tparam):
            self.errors.append(f"El parametro '{nparam}' ya esta definido")

###########################################################  

    @visitor.when(IfEndNode)
    def visit(self, node: IfEndNode, scope: Scope):
        self.visit(node.cond, scope)
        child = scope.create_child_scope()
        for st in node.statements:
            self.visit(st, child) 

    @visitor.when(IfElseEndNode)
    def visit(self, node: IfElseEndNode, scope: Scope):
        self.visit(node.cond, scope)
        child_if = scope.create_child_scope()
        child_else = scope.create_child_scope()

        for st in node.statements_if:
            self.visit(st, child_if)
        for st in node.statements_else:
            self.visit(st, child_else)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        self.visit(node.cond, scope)
        child = scope.create_child_scope()
        for st in node.statements:
            self.visit(st, child)

###########################################################  
    
    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):        
        try:
            value = float(node.lex)
            node.lex = value
        except:
            self.errors.append('No se puede convertir a float')
    
    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope: Scope):        
        try:
            value = bool(node.lex)
            node.lex = value
        except:
            self.errors.append('No se puede convertir a bool')
    
    @visitor.when(VarConstNode)
    def visit(self, node: VarConstNode, scope: Scope):        
        if not scope.is_var_defined(node.lex) and not scope.is_const_defined(node.lex):
            self.errors.append(f"No existe ninguna variable o constante '{node.lex}' definida.")
    
    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):        
        if not scope.is_func_defined(node.lex):
            self.errors.append(f'La funcion {node.lex} no ha sido definida')
        for arg in node.args:            
            self.visit(arg, scope)    
    
    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope: Scope):        
        self.visit(node.left, scope)
        self.visit(node.right, scope) 