try:
    import visitor
except:
    from utils06 import visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

##################################
class ProgramNode(Node):
    def __init__(self, sec_maps, sec_inst):
        self.sec_maps = sec_maps
        self.sec_inst = sec_inst

class SecMapsNode(Node):
    def __init__(self, maps) -> None:
        self.maps = maps

class SecInstructionNode(Node):
    def __init__(self, instructions) -> None:
        self.instructions = instructions

##################################
#            .MAPS               #
##################################

class MapDeclaration(Node):
    def __init__(self, idx, map) -> None:
        self.id = idx
        self.map = map    

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class SquareNode(AtomicNode):
    pass


##################################
#            .INST               #
##################################
class InstructionNode(Node):
    pass

class AtomicInstructionNode(InstructionNode):
    def __init__(self, lex):
        self.lex = lex 

class MovNode(AtomicInstructionNode):
    pass

class GotoNode(AtomicInstructionNode):
    pass

class GotoIfZeroNode(AtomicInstructionNode):
    pass

class GotoIfPositive(AtomicInstructionNode):
    pass

class GotoIfNegative(AtomicInstructionNode):
    pass

class LabelNode(AtomicInstructionNode):
    pass

class OverlapNode(AtomicInstructionNode):
    pass

class PullNode(InstructionNode):
    pass

class PushNode(InstructionNode):
    pass

class PopNode(InstructionNode):
    pass

class CopyNode(InstructionNode):
    pass

class PasteNode(InstructionNode):
    pass

class AddNode(InstructionNode):
    pass

class SubNode(InstructionNode):
    pass

class DivNode(InstructionNode):
    pass

class MulNode(InstructionNode):
    pass

class ModNode(InstructionNode):
    pass

class DecNode(InstructionNode):
    pass

class IncNode(InstructionNode):
    pass

class PushMem(InstructionNode):
    pass

class PopMem(InstructionNode):
    pass
