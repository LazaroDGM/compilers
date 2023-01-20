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
    def __init__(self, id, reserving, instructions) -> None:
        self.id = id
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

class OperationInstructionNode(InstructionNode):
    pass

###################################

class OperationNode(Node):
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

class IncNode(BinaryOperationNode):
    pass

class DecNode(BinaryOperationNode):
    pass

class EqualNode(BinaryOperationNode):
    pass

class NotEqualNode(BinaryOperationNode):
    pass

class LessThanNode(BinaryInstruction):
    pass

class LessThanEqualNode(BinaryInstruction):
    pass

class LessThanNode(BinaryInstruction):
    pass

class GreaterThanNode(BinaryInstruction):
    pass

class GreaterThanEqualNode(BinaryInstruction):
    pass
#######################################

class PrintNode(AtomicOperationNode):
    pass

#######################################

class TupleNode(BinaryNode):
    pass


