class VariableInfo:
    def __init__(self, name):
        self.name = name

class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Scope:
    def __init__(self, parent=None):
        self.local_vars = []
        self.local_funcs = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname):
        # Your code here!!!
        if not self.is_var_defined(vname):
            vinfo = VariableInfo(vname)
            self.local_vars.append(vinfo)
            return True
        return False
    
    def define_function(self, fname, params):
        # Your code here!!!
        if not self.is_func_defined(fname, params):
            finfo = FunctionInfo(fname, params)
            self.local_funcs.append(finfo)
            return True
        return False

    def is_var_defined(self, vname):
        # Your code here!!!   
        child = self
        while child is not None:            
            vinfo = self.get_local_variable_info(vname)
            if vinfo is not None:
                return True
            child = self.parent
        return False
    
    
    def is_func_defined(self, fname, n):
        # Your code here!!!
        child = self
        while child is not None:            
            finfo = self.get_local_function_info(fname, n)
            if finfo is not None:
                return True
            child = self.parent
        return False


    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname):
        # Your code here!!!        
        for vinfo in self.local_vars:
            if vinfo.name == vname:
                return vinfo        
        return None        
    
    def get_local_function_info(self, fname, n):
        # Your code here!!!        
        for finfo in self.local_funcs:
            if finfo.name == fname and len(finfo.params) == n:
                return finfo        
        return None