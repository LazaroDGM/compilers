try:
    import visitor
except:
    from utils07 import visitor

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
        self.instructions.append(NopNode)

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

class GotoGeneric(AtomicInstructionNode):
    pass

class GotoNode(GotoGeneric):
    pass

class GotoIfZeroNode(GotoGeneric):
    pass

class GotoIfPositive(GotoGeneric):
    pass

class GotoIfNegative(GotoGeneric):
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

class PushMemNode(InstructionNode):
    pass

class PopMemNode(InstructionNode):
    pass

class NopNode(InstructionNode):
    pass

class PrintNode(InstructionNode):
    pass