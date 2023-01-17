from tools.shift_reduce import LR1Parser, evaluate_reverse_parse
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
from tools.ast import Node, BinaryNode, get_printer

class ConstantNumberNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = float(lex)
        
    def evaluate(self):        
        return self.value

class EqualComparerNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):     
        return lvalue == rvalue

class NotEqualComparerNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):     
        return lvalue != rvalue

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

class Language04:
    def __init__(self) -> None:
        ########################################################
        #                 GRAMATICA 04  LR(1)                  #        
        ########################################################
        G = Grammar()
        S = G.NonTerminal('S', True)
        E,T,F = G.NonTerminals('E T F')
        plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) int')
        equal_comp, not_equal_comp = G.Terminals('== !=')

        S %= E + equal_comp + E, lambda h,s: EqualComparerNode(s[1], s[3])
        S %= E + not_equal_comp + E, lambda h,s: NotEqualComparerNode(s[1], s[3])
        
        E %= E + plus + T, lambda h,s: PlusNode(s[1], s[3])
        E %= E + minus + T, lambda h, s: MinusNode(s[1], s[3])
        E %= T, lambda h, s: s[1]

        T %= T + star + F, lambda h, s: StarNode(s[1], s[3])
        T %= T + div + F, lambda h, s: DivNode(s[1], s[3])
        T %= F, lambda h, s: s[1]

        F %= num, lambda h, s: ConstantNumberNode(s[1])
        F %= opar + E + cpar, lambda h, s: s[2]
        
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

                (equal_comp, '=='),
                (not_equal_comp, '!='),

                (opar, '\('),
                (cpar, '\)'),                
            ], G.EOF
        )
        self.lexer = lexer
        ########################################################
        #                    PARSER LR(1)                      #
        ########################################################
        parser = LR1Parser(G)
        self.parser = parser

        ########################################################
        #                       PRINTER                        #
        ########################################################
        self.printer = get_printer(AtomicNode=ConstantNumberNode, BinaryNode=BinaryNode)
    
    ####################################
    #                AST               #
    ####################################
    def Build_AST(self, text, verbose=False):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        right_parse, operations = self.parser(tokens)        
        ast = evaluate_reverse_parse(right_parse, operations, tokens)

        if verbose:
            self.Print(ast)
        return ast

    ####################################
    #           EVALUATE               #
    ####################################
    def Evaluate(self, text, verbose= False):
        ast = self.Build_AST(text, verbose)
        result = ast.evaluate()

        return result 

    ####################################
    #              VALID               #
    ####################################
    def is_Valid(self, text, verbose=False):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        right_parse, operations = self.parser(tokens)  
        return True 

    def Print(self, ast):
        print(self.printer(ast))
