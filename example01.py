from tools.parserLL1 import parser_LL1_generator
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token

class Node:
    def evaluate(self):
        raise NotImplementedError()

class ConstantNumberNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = float(lex)
        
    def evaluate(self):        
        return self.value
        

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue =  self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()
        

class PlusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        return lvalue + rvalue        

class MinusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        return lvalue - rvalue

class StarNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        lvalue * rvalue

class DivNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        lvalue / rvalue

class PowNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        lvalue ** rvalue

