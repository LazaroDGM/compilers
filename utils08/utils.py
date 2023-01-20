try:
    import visitor
except:
    from utils08 import visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

##################################
class ProgramNode(Node):
    def __init__(self, sec_maps, sec_inst):
        self.sec_maps = sec_maps
        self.sec_inst = sec_inst