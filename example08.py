from tools.shift_reduce import evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token, SintacticException
from utils08.utils import *

class Language08:
    def __init__(self) -> None:
        ########################################################
        #                GRAMATICA 08  SLR(1)                  #        
        ########################################################

        G = Grammar()

        program = G.NonTerminal('<program>', startSymbol=True)
        def_list, defx,  map_def, function_def = G.NonTerminals('<def-list> <def> <map-def> <function-def>')

        tuple_list, tuplex, hamper, num, num_list = \
            G.NonTerminals('<tuple-list> <tuple> <hamper> <num> <num_list>')
        asign_pos_list, asign_pos, type_pos= G.NonTerminals('<asign_pos_list> <asig-pos> <pos>')

        inst_list, inst = G.NonTerminals('<inst_list> <inst>')
        let_tuple, op_inst, if_inst, while_inst, call_func, print_inst, cond = \
            G.NonTerminals('<let-tuple> <op-inst> <if-inst> <while-inst> <call-func> <printx-inst> <cond>')


        semi, comma, obrac, cbrac, okey, ckey, colon, opar, cpar = G.Terminals('; , [ ] { } : ( )')
        idx, number = G.Terminals('ID NUMBER')
        mapx, functionx, robil = G.Terminals('map function .ROBIL')
        inx, withx, ifx, elsex, whilex, then, endif, endwhile, reserving, callx, printx = \
            G.Terminals('in with if else while then endif endwhile reserving call print')

        eq, neq, lte, gte, lt, gt = G.Terminals('== != <= >= < >')
        asign, plus, minus, star, div = G.Terminals('= + - * /')

        program %= robil + def_list, lambda h,s: s[2]

        def_list %= defx + def_list, lambda h,s: [ s[1] ] + s[2]
        def_list %= defx,lambda h,s: [ s[1] ]

        defx %= map_def, lambda h,s: s[1]
        defx %= function_def, lambda h,s: s[1]

        map_def %= mapx + idx + tuplex + okey + asign_pos_list + ckey, lambda h,s: MapDefinitionNode(s[2], s[3], s[5])
        map_def %= mapx + idx + tuplex + okey + ckey, lambda h,s: MapDefinitionNode(s[2], s[3], [])

        asign_pos_list %= asign_pos + asign_pos_list, lambda h,s: [ s[1] ] + s[2]
        asign_pos_list %= asign_pos, lambda h,s: [ s[1] ]

        asign_pos %= tuplex + asign + number + semi, lambda h,s: NumberAsignNode(s[1], s[3])
        asign_pos %= tuplex + asign + hamper + semi, lambda h,s: HamperAsignNode(s[1], s[3])

        hamper %= obrac + num_list + cbrac, lambda h,s: s[2]
        hamper %= obrac + cbrac, lambda h,s: []

        num_list %= number + comma + num_list, lambda h,s: [ s[1] ] + s[3]
        num_list %= number, lambda h,s: [ s[1] ]


        function_def %= functionx + idx + inx + idx + reserving + tuple_list + okey + inst_list + ckey
        function_def %= functionx + idx + inx + idx + okey + inst_list + ckey

        tuple_list %= tuplex + comma + tuple_list, lambda h,s: [ s[1] ] + s[3]
        tuple_list %= tuplex, lambda h,s: [ s[1] ]

        inst_list %= inst + inst_list, lambda h,s: [ s[1] ] + s[3]
        inst_list %= inst, lambda h,s: [ s[1] ]

        inst %= let_tuple, lambda h,s: s[1]
        inst %= op_inst, lambda h,s: s[1]
        inst %= call_func, lambda h,s: s[1]
        inst %= if_inst, lambda h,s: s[1]
        inst %= while_inst, lambda h,s: s[1]
        inst %= print_inst, lambda h,s: s[1]

        let_tuple %= tuplex + asign + tuplex + semi, lambda h,s: LetTupleFromTupleNode(s[1], s[3])
        let_tuple %= tuplex + asign + tuplex + obrac + number + cbrac + semi, lambda h,s: LetTupleFromHamperNode(s[1], s[3], s[5])

        op_inst %= tuplex + asign + tuplex + plus + tuplex + semi, lambda h,s: PlusNode(s[1], s[3], s[5])
        op_inst %= tuplex + asign + tuplex + minus + tuplex + semi, lambda h,s: MinusNode(s[1], s[3], s[5])
        op_inst %= tuplex + asign + tuplex + star + tuplex + semi, lambda h,s: StarNode(s[1], s[3], s[5])
        op_inst %= tuplex + asign + tuplex + div + tuplex + semi, lambda h,s: DivNode(s[1], s[3], s[5])

        op_inst %= tuplex + plus + plus + semi, lambda h,s: IncNode(s[1])
        op_inst %= tuplex + minus + minus + semi, lambda h,s: DecNode(s[1])

        call_func %= tuplex + asign + callx + idx + withx + tuple_list + semi
        call_func %= tuplex + asign + callx + idx + semi

        tuplex %= opar + number + comma + number + cpar, lambda h,s: TupleNode(s[2], s[4])

        if_inst %= ifx + cond + then + inst_list + endif, lambda h,s: IfEndNode(s[2], s[4])
        if_inst %= ifx + cond + then + inst_list + elsex +inst_list + endif, lambda h,s: IfElseEndNode(s[2], s[4], s[6])

        while_inst %= whilex + cond + then + inst_list + endwhile, lambda h,s: WhileNode(s[2], s[4])

        cond %= tuplex + eq + tuplex, lambda h,s: EqualNode(s[1], s[3])
        cond %= tuplex + neq + tuplex, lambda h,s: NotEqualNode(s[1], s[3])
        cond %= tuplex + lt + tuplex, lambda h,s: LessThanNode(s[1], s[3])
        cond %= tuplex + lte + tuplex, lambda h,s: LessThanEqualNode(s[1], s[3])
        cond %= tuplex + gt + tuplex, lambda h,s: GreaterThanNode(s[1], s[3])
        cond %= tuplex + gte + tuplex, lambda h,s: GreaterThanEqualNode(s[1], s[3])

        print_inst %= printx + tuplex + semi, lambda h,s: PrintNode(s[2])

        ########################################################
        #                    PARSER SLR(1)                     #
        ########################################################
        parser = SLR1Parser(G)
        self.parser = parser

        ########################################################
        #                        LEXER                         #
        ########################################################
        nonzero_digits = '|'.join(str(n) for n in range(1,10))
        letters_lower = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
        letters_power = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
        lexer = Lexer(
            [
                ('space', '( |\t|\n)( |\t|\n)*'),  

                (robil, '\.ROBIL'),

                (comma, ','),
                (semi,';'),
                (asign,'='),
                (okey, '{'),
                (ckey, '}'),
                (opar, '\('),
                (cpar,'\)'),
                (colon,':'),

                (plus,'\+'),
                (minus,'-'),
                (star, '\*'),
                (div, '/'),

                (eq,'=='),
                (neq,'!='),
                (lte,'<='),
                (gte,'>='),
                (lt,'<'),
                (gt,'>'),                

                (inx, 'in'),
                (withx, 'with'),
                (ifx, 'if'),
                (elsex, 'else'),
                (whilex, 'while'),
                (then, 'then'),
                (endif, 'endif'),
                (endwhile, 'endwhile'),
                (reserving, 'reserving'),
                (callx, 'call'),
                (printx, 'print'),

                (mapx, 'map'),
                (functionx, 'function'),
                
                (number,f'({nonzero_digits})(0|{nonzero_digits})*|0'),
                (idx, f'({letters_lower}|{letters_power})({letters_lower}|{letters_power}|{nonzero_digits}|0)*')

            ],
            G.EOF
        )
        self.lexer = lexer

    def Parse_Tokens(self, tokens):
        right_parse, operations = None, None
        try:
            right_parse, operations = self.parser(tokens)
        except SintacticException as e:
            print(e)
        except Exception as e:
            print('Ocurrio un error durante el Parseo')
        return right_parse, operations

    ####################################
    #              VALID               #
    ####################################
    def is_Valid_Sintactic(self, text, verbose=False):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        right_parse, operations = self.Parse_Tokens(tokens) 
        if right_parse is None or operations is None:
            return False
        return True


text=\
'''
.ROBIL

map M1 (4,5){
    (0,0) = 0;
    (1,0) = 5;
    (1,1) = 1;
    (0,1) = 2;
}

function MAIN in M1{

    while (1,0) == (0,0) then
        (1,1) = (0,1) * (1,1);
        (1,0)--;
    endwhile

    print (1,1);
}
'''


L  =Language08()
L.is_Valid_Sintactic(text)
