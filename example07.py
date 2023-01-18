from tools.shift_reduce import evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token

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

        
        program %= maps_sec + inst_sec

        ###########  .MAPS #####################
        maps_sec %= sec_map_name + okey + maps_list + ckey

        maps_list %= def_map + maps_list
        maps_list %= def_map

        def_map %= mapx + idx + colon + body_map

        body_map %= obrac + rows_map + cbrac

        rows_map %= obrac + row_map + cbrac + comma + rows_map
        rows_map %= obrac + row_map + cbrac

        row_map %= square + comma + row_map
        row_map %= square

        square %= squarex
        square %= numx

        ##########  .INST ######################
        inst_sec %= sec_inst_name + okey + inst_list + ckey

        inst_list %= inst + inst_list
        inst_list %= inst

        inst %= mov_i
        inst %= copy_i
        inst %= paste_i

        inst %= add_i
        inst %= sub_i
        inst %= mul_i
        inst %= div_i
        inst %= mod_i
        inst %= inc_i
        inst %= dec_i

        inst %= goto_i
        inst %= label_i
        inst %= overlap_i
        inst %= pull_i
        inst %= push_i
        inst %= pop_i

        mov_i %= mov + dirx + semi
        copy_i %= copy + semi
        paste_i %= paste + semi

        add_i %= add + semi
        sub_i %= sub + semi
        mul_i %= mul + semi
        div_i %= div + semi
        mod_i %= mod + semi        
        dec_i %= dec + semi
        inc_i %= inc + semi

        label_i %= label + idx + colon
        overlap_i %= overlap + idx + semi
        pull_i %= pull + semi
        push_i %= push + semi
        pop_i %= pop + semi

        goto_i %= goto + idx + semi
        goto_i %= goto + idx + ifzero + semi
        goto_i %= goto + idx + ifpositive + semi
        goto_i %= goto + idx + ifnegative + semi

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
    overlap M1;
    
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