try:
    import visitor
except:
    from utils06 import visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

##################################
class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements
        
class StatementNode(Node):
    pass

#################################

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, ttype, expr):        
        self.id = idx
        self.ttype= ttype
        self.expr = expr

class ConstDeclarationNode(StatementNode):
    def __init__(self, idx, ttype, expr):        
        self.id = idx
        self.ttype= ttype
        self.expr = expr

class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, types, params, return_type, body):
        self.id = idx
        self.types= types
        self.params = params
        self.body = body

class AsignVarNode(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr

class IfEndNode(StatementNode):
    def __init__(self, cond, statements) -> None:        
        self.cond = cond
        self.statements = statements

class IfElseEndNode(StatementNode):
    def __init__(self, cond, statements_if, statements_else) -> None:        
        self.cond = cond
        self.statements_if = statements_if
        self.statements_else = statements_else

class WhileNode(StatementNode):
    def __init__(self, cond, statements) -> None:        
        self.cond = cond
        self.statements = statements  

class ReturnNode(StatementNode):
    def __init__(self, expr) -> None:        
        self.expr = expr        

##############################################

class ParamListNode(Node):
    def __init__(self, idxs, ttypes):
        self.ids = idxs
        self.ttypes= ttypes

class ParamNode(Node):
    def __init__(self, idx, ttype):
        self.id = idx
        self.ttype= ttype

##############################################

class ExpressionNode(Node):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex        

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

##################################

class AndNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

###################################

class EqualNode(BinaryNode):
    pass

class NotEqualNode(BinaryNode):
    pass

class LessThanEqualNode(BinaryNode):
    pass

class GreaterEqualNode(BinaryNode):
    pass

class LessThanNode(BinaryNode):
    pass

class GreaterNode(BinaryNode):
    pass

####################################

class ConstantNumNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class BoolNode(AtomicNode):
    pass

class CallNode(AtomicNode):
    def __init__(self, idx, args):
        AtomicNode.__init__(self, idx)
        self.args = args

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass