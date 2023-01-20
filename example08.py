from tools.shift_reduce import evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token, SintacticException

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

        program %= robil + def_list

        def_list %= defx + def_list
        def_list %= defx

        defx %= map_def
        defx %= function_def

        map_def %= mapx + idx + tuplex + okey + asign_pos_list + ckey
        map_def %= mapx + idx + tuplex + okey + ckey

        asign_pos_list %= asign_pos + asign_pos_list
        asign_pos_list %= asign_pos

        asign_pos %= tuplex + asign + type_pos + semi

        type_pos %= number
        type_pos %= hamper

        hamper %= obrac + num_list + cbrac
        hamper %= obrac + cbrac

        num_list %= number
        num_list %= number + comma + num_list


        function_def %= functionx + idx + inx + idx + reserving + tuple_list + okey + inst_list + ckey
        function_def %= functionx + idx + inx + idx + okey + inst_list + ckey

        tuple_list %= tuplex + comma + tuple_list
        tuple_list %= tuplex

        inst_list %= inst + inst_list
        inst_list %= inst

        inst %= let_tuple
        inst %= op_inst
        inst %= call_func
        inst %= if_inst
        inst %= while_inst
        inst %= print_inst

        let_tuple %= tuplex + asign + tuplex + semi
        let_tuple %= tuplex + asign + tuplex + obrac + number + cbrac + semi

        op_inst %= tuplex + asign + tuplex + plus + tuplex + semi
        op_inst %= tuplex + asign + tuplex + minus + tuplex + semi
        op_inst %= tuplex + asign + tuplex + star + tuplex + semi
        op_inst %= tuplex + asign + tuplex + div + tuplex + semi

        op_inst %= tuplex + plus + plus + semi
        op_inst %= tuplex + minus + minus + semi

        call_func %= tuplex + asign + callx + idx + withx + tuple_list + semi
        call_func %= tuplex + asign + callx + idx + semi

        tuplex %= opar + number + comma + number + cpar

        if_inst %= ifx + cond + then + inst_list + endif
        if_inst %= ifx + cond + then + inst_list + elsex +inst_list + endif

        while_inst %= whilex + cond + then + inst_list + endwhile

        cond %= tuplex + eq + tuplex
        cond %= tuplex + neq + tuplex
        cond %= tuplex + lt + tuplex
        cond %= tuplex + lte + tuplex
        cond %= tuplex + gt + tuplex
        cond %= tuplex + gte + tuplex

        print_inst %= printx + tuplex + semi

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
