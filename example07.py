from tools.shift_reduce import evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
from utils07.utils import *
from utils07.type_collector import TypeCollector

class Language07:
    def __init__(self) -> None:
        ########################################################
        #                GRAMATICA 07  SLR(1)                  #        
        ########################################################

        G = Grammar()

        ############  Program  ##############
        program = G.NonTerminal('<program>', startSymbol=True)
        ############ .MAPS #############
        maps_sec, maps_list, def_map = G.NonTerminals('<maps-sec> <maps-list> <def-map>')
        body_map, rows_map, row_map, square_list, square =G.NonTerminals('<body-map> <rows-map> <row-map> <square-list> <square>')
        ############ .INST #############
        inst_sec, inst_list, inst = G.NonTerminals('<inst-sec> <inst-list> <inst>')
        mov_i, copy_i, paste_i = G.NonTerminals('<mov> <copy> <paste>')
        add_i, sub_i, mul_i, div_i, mod_i, inc_i, dec_i = G.NonTerminals('<add> <sub> <mul> <div> <mod> <inc> <dec>')
        goto_i, label_i = G.NonTerminals('<goto> <label>')
        push_i, pop_i, push_mem, pop_mem, overlap_i, pull_i = G.NonTerminals('<push> <pop> <push-mem> <pop-mem> <overlap> <pull>')


        dirx, idx, squarex, numx = G.Terminals('DIR ID SQUARE NUMBER')
        semi, comma, obrac, cbrac, okey, ckey, colon = G.Terminals('; , [ ] { } :')
        
        sec_map_name, sec_inst_name = G.Terminals('.MAPS .INST')

        mov, copy, paste, mapx = G.Terminals('mov copy paste map')
        add, sub, mul, div, mod, inc, dec = G.Terminals('add sub mul div mod inc dec')
        goto, label, ifzero, ifpositive, ifnegative = G.Terminals('goto label ifzero ifpositive ifnegative')
        push, pop, mem, overlap, pull = G.Terminals('push pop mem overlap pull')

        
        program %= maps_sec + inst_sec, lambda h,s: ProgramNode(s[1], s[2])

        ###########  .MAPS #####################
        maps_sec %= sec_map_name + okey + maps_list + ckey, lambda h,s: SecMapsNode(s[3])

        maps_list %= def_map + maps_list, lambda h,s: [ s[1] ] + s[2]
        maps_list %= def_map, lambda h,s: [ s[1] ]

        def_map %= mapx + idx + colon + body_map, lambda h,s: MapDeclaration(idx= s[2], map= s[4])

        body_map %= obrac + rows_map + cbrac, lambda h,s: s[2]

        rows_map %= obrac + row_map + cbrac + comma + rows_map, lambda h,s: [ s[2] ] + s[5]
        rows_map %= obrac + row_map + cbrac, lambda h,s: [ s[2] ]

        row_map %= square + comma + row_map,lambda h,s: [ s[1] ] + s[3]
        row_map %= square, lambda h,s: [ s[1] ]

        square %= squarex, lambda h,s: SquareNode(s[1])
        square %= numx, lambda h,s: SquareNode(s[1])

        ##########  .INST ######################
        inst_sec %= sec_inst_name + okey + inst_list + ckey, lambda h,s: SecInstructionNode(s[3])

        inst_list %= inst + inst_list, lambda h,s: [ s[1] ] + s[2]
        inst_list %= inst, lambda h,s: [ s[1] ]

        inst %= mov_i, lambda h,s: s[1]
        inst %= copy_i, lambda h,s: s[1]
        inst %= paste_i, lambda h,s: s[1]

        inst %= add_i, lambda h,s: s[1]
        inst %= sub_i, lambda h,s: s[1]
        inst %= mul_i, lambda h,s: s[1]
        inst %= div_i, lambda h,s: s[1]
        inst %= mod_i, lambda h,s: s[1]
        inst %= inc_i, lambda h,s: s[1]
        inst %= dec_i, lambda h,s: s[1]

        inst %= goto_i, lambda h,s: s[1]
        inst %= label_i, lambda h,s: s[1]
        inst %= overlap_i, lambda h,s: s[1]
        inst %= pull_i, lambda h,s: s[1]
        inst %= push_i, lambda h,s: s[1]
        inst %= pop_i, lambda h,s: s[1]

        mov_i %= mov + dirx + semi, lambda h,s: MovNode(s[2])
        copy_i %= copy + semi, lambda h,s: CopyNode()
        paste_i %= paste + semi, lambda h,s: PasteNode()

        add_i %= add + semi, lambda h,s: AddNode()
        sub_i %= sub + semi, lambda h,s: SubNode()
        mul_i %= mul + semi, lambda h,s: MulNode()
        div_i %= div + semi, lambda h,s: DivNode()
        mod_i %= mod + semi, lambda h,s: ModNode()
        dec_i %= dec + semi, lambda h,s: DecNode()
        inc_i %= inc + semi, lambda h,s: IncNode()

        label_i %= label + idx + colon, lambda h,s: LabelNode(s[2])
        overlap_i %= overlap + idx + semi, lambda h,s: OverlapNode(s[2])
        pull_i %= pull + semi, lambda h,s: PullNode()
        push_i %= push + semi, lambda h,s: PushNode()
        pop_i %= pop + semi, lambda h,s: PopNode()

        goto_i %= goto + idx + semi, lambda h,s: GotoNode(s[2])
        goto_i %= goto + idx + ifzero + semi, lambda h,s: GotoIfZeroNode(s[2])
        goto_i %= goto + idx + ifpositive + semi, lambda h,s: GotoIfPositive(s[2])
        goto_i %= goto + idx + ifnegative + semi, lambda h,s: GotoIfNegative(s[2])

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

                (squarex, 'H|V|(({nonzero_digits})(0|{nonzero_digits})*)|0'),
                (dirx, 'N|S|E|W'),

                (sec_map_name, '\.MAPS'),
                (sec_inst_name, '\.INST'),

                (semi,';'),
                (comma, ','),
                (obrac, '\['),
                (cbrac, '\]'),
                (okey, '{'),
                (ckey, '}'),
                (colon,':'),

                (mov, 'mov'),
                (copy, 'copy'),
                (paste, 'paste'),

                (add, 'add'),
                (sub, 'sub'),
                (mul, 'mul'),
                (div, 'div'),
                (mod, 'mod'),
                (dec, 'dec'),
                (inc, 'inc'),

                (pop, 'pop'),
                (push, 'push'),
                (overlap, 'overlap'),
                (pull, 'pull'),

                (goto, 'goto'),
                (ifzero, 'ifzero'),
                (ifpositive, 'ifpositive'),
                (ifnegative, 'ifnegative'),
                (label, 'label'),

                (mapx, 'map'),
                
                (numx,f'({nonzero_digits})(0|{nonzero_digits})*'),                
                (idx, f'({letters_lower}|{letters_power})({letters_lower}|{letters_power}|{nonzero_digits}|0)*')

            ],
            G.EOF
        )
        self.lexer = lexer
        ########################################################
        # ==================================================== #
        ########################################################
    
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
    #              VALID               #
    ####################################
    def is_Valid(self, text, verbose=False):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        right_parse, operations = self.parser(tokens)  
        return True

L = Language07()

text = '''
.MAPS{
    map M1:
    [
        [V,V,V,V],
        [V,V,V,V],
        [V,V,V,V]
    ]

    map M2:
    [
        [0,V,V,V],
        [5,2,V,V],
        [V,V,V,V]
    ]
}

.INST{
    overlap M2;
    
    mov S;
    mov S;
    mov E;
    mov E;
    mov E;
    mov E;
    mov N;
    mov W;
    mov W;
    mov N;
    mov E;

    mov S;

label WHILE:
    copy;
    dec;
    goto ENDWHILE ifzero;

    mov E;
    copy;
    add;
    paste;

    mov W;
    goto WHILE;

    copy;
    add;
    copy;

label ENDWHILE:
    mov E;
    copy;

}
'''

L.is_Valid(text)
ast = L.Build_AST(text)

type_collector = TypeCollector()
errors, context = type_collector.visit(ast)
for i, error in enumerate(errors, 1):
    print(f'{i}.', error)

print(context)