from tools.shift_reduce import LR1Parser, evaluate_reverse_parse
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
from tools.ast import Node, BinaryNode, get_printer

class Language03:
    def __init__(self) -> None:
        ########################################################
        #                 GRAMATICA 03  LR(1)                  #        
        ########################################################
        G = Grammar()
        E = G.NonTerminal('E', True)
        A = G.NonTerminal('A')
        equal, plus, num = G.Terminals('= + int')

        E %=  A + equal + A | num
        A %= num + plus + A | num
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

                (equal, '='),
                (plus, '\+'),
               
            ], G.EOF
        )
        self.lexer = lexer
        ########################################################
        #                    PARSER LR(1)                     #
        ########################################################
        parser = LR1Parser(G)
        self.parser = parser
        

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