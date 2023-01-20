try:
    import visitor
except:
    from utils08 import visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

##################################
class ProgramNode(Node):
    def __init__(self, defs):
        self.defs = defs

##################################

class DefinitionNode(Node):
    pass

class MapDefinitionNode(DefinitionNode):
    def __init__(self, map) -> None:
        self.map = map

class FunctionDefinitionNode(DefinitionNode):
    def __init__(self, id, reserving, instructions) -> None:
        self.id = id
        self.reserving = reserving
        self.instructions = instructions

###################################
############# Maps ################
###################################



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

###################################

class LetTupleNode(AtomicInstruction):
    pass

class OperationInstructionNode(BinaryInstruction):
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

#######################################
class PlusNode(BinaryOperationNode):
    pass

class MinusNode(BinaryOperationNode):
    pass

class StarNode(BinaryOperationNode):
    pass

class DivNode(BinaryOperationNode):
    pass

class IncNode(AtomicOperationNode):
    pass

class DecNode(AtomicOperationNode):
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


