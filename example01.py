from tools.parserLL1 import parser_LL1_generator, evaluate_parse
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
import tools.visitor as visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

class ConstantNumberNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = float(lex)
        
    def evaluate(self):        
        return self.value

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
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
        return lvalue * rvalue

class DivNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        return lvalue / rvalue

class PowNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue




class Language01:
    def __init__(self) -> None:
        ########################################################
        #                 GRAMATICA 01  LL(1)                  #
        #                     ATRIBUTADA                       #
        ########################################################
        G = Grammar()
        E = G.NonTerminal('E', True)
        T, F, X, Y = G.NonTerminals('T F X Y')
        plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')


        E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

        X %= plus + T + X, lambda h, s: s[3], None, None, lambda h,s: PlusNode(h[0], s[2])
        X %= minus + T + X, lambda h, s: s[3], None, None, lambda h,s: MinusNode(h[0], s[2])
        X %= G.Epsilon, lambda h, s: h[0]

        T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

        Y %= star + F + Y, lambda h,s: s[3], None, None, lambda h, s: StarNode(h[0], s[2])
        Y %= div + F + Y, lambda h,s: s[3], None, None, lambda h, s: DivNode(h[0], s[2])
        Y %= G.Epsilon, lambda h, s: h[0]

        F %= num, lambda h, s: ConstantNumberNode(s[1]), None
        F %= opar + E + cpar, lambda h, s: s[2], None, None, None

        ########################################################
        # ==================================================== #
        ########################################################


        ########################################################
        #                        LEXER                         #
        ########################################################
        lexer = Lexer(
            [
                (num, '(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'),

                ('space', '( |\t|\n)( |\t|\n)*'),

                (plus, '\+'),
                (minus, '-'),
                (star, '\*'),
                (div, '/'),

                (opar, '\('),
                (cpar, '\)'),                
            ], G.EOF
        )
        self.lexer = lexer
        ########################################################
        #                    PARSER LL(1)                      #
        ########################################################
        parser = parser_LL1_generator(G)
        self.parser = parser

    def Build_AST(self, text):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        left_parse = self.parser(tokens)        
        ast = evaluate_parse(left_parse, tokens)

        return ast

    def Evaluate(self, text):
        ast = self.Build_AST(text)
        result = ast.evaluate()

        return result