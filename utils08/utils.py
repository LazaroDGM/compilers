try:
    import visitor
except:
    from utils08 import visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode:
    def __init__(self, lex) -> None:
        self.lex = lex

class BinaryNode:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

##################################
class ProgramNode(Node):
    def __init__(self, defs):
        self.defs = defs

##################################

class DefinitionNode(Node):
    pass

class MapDefinitionNode(DefinitionNode):
    def __init__(self, id, map, asigns) -> None:
        self.id = id
        self.map = map
        self.asigns = asigns

class FunctionDefinitionNode(DefinitionNode):
    def __init__(self, id_func, id_map, reserving, instructions) -> None:
        self.id_func = id_func
        self.id_map = id_map
        self.reserving = reserving
        self.instructions = instructions

###################################
############# Maps ################
###################################


class AsignNode(Node):
    pass

class BinaryAsignNode(AsignNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

class TernaryAsignNode(AsignNode):
    def __init__(self, left, center, right) -> None:
        self.left = left
        self.center = center
        self.right = right

class NumberAsignNode(BinaryAsignNode):
    pass

class HamperAsignNode(BinaryAsignNode):
    pass

###################################
############# Func ################
###################################

class InstructionNode(Node):
    pass

class AtomicInstruction(InstructionNode):
    def __init__(self, lex) -> None:
        self.lex = lex

class BinaryInstruction(InstructionNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

class TernaryInstruction(InstructionNode):
    def __init__(self, left, center, right) -> None:
        self.left = left
        self.center = center
        self.right = right

###################################

class LetTupleFromTupleNode(BinaryInstruction):
    pass

class LetTupleFromHamperNode(TernaryInstruction):
    pass       

class IfEndNode(InstructionNode):
    def __init__(self, cond, instructions_if) -> None:
        self.cond = cond 
        self.instructions_if = instructions_if

class IfElseEndNode(IfEndNode):
    def __init__(self, cond, instructions_if, instructions_else) -> None:
        super().__init__(cond, instructions_if)
        self.instructions_else = instructions_else

class WhileNode(InstructionNode):
    def __init__(self, cond, instructions_while) -> None:
        self.cond = cond 
        self.instructions_while = instructions_while

class CallFunctionNode(InstructionNode):
    def __init__(self, tuple, id, tuple_list) -> None:
        self.tuple = tuple
        self.id = id
        self.tuple_list = tuple_list

class ReturnIstruction(InstructionNode):
    def __init__(self, tuple) -> None:
        self.tuple= tuple


###################################

class OperationNode(InstructionNode):
    pass

class AtomicOperationNode(OperationNode):
    def __init__(self, lex) -> None:
        self.lex = lex

class BinaryOperationNode(OperationNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

class TernaryOperationNode(OperationNode):
    def __init__(self, left, center, right) -> None:
        self.left = left
        self.center = center
        self.right = right

#######################################
class PlusNode(TernaryOperationNode):
    pass

class MinusNode(TernaryOperationNode):
    pass

class StarNode(TernaryOperationNode):
    pass

class DivNode(TernaryOperationNode):
    pass

class IncNode(AtomicOperationNode):
    pass

class DecNode(AtomicOperationNode):
    pass

#######################################

class CondNode():
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

class EqualNode(CondNode):
    pass

class NotEqualNode(CondNode):
    pass

class LessThanNode(CondNode):
    pass

class LessThanEqualNode(CondNode):
    pass

class LessThanNode(CondNode):
    pass

class GreaterThanNode(CondNode):
    pass

class GreaterThanEqualNode(CondNode):
    pass
#######################################

class PrintNode(AtomicOperationNode):
    pass

#######################################

class TupleNode(BinaryNode):
    def tup(self):
        return (self.left, self.right)

#######################################