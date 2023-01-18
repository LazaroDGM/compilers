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
        add_i, sub_i, mul_i, div_i, mod_i = G.NonTerminals('<add> <sub> <mul> <div> <mod>')
        goto_i, label_i = G.NonTerminals('<goto> <label>')
        push_i, pop_i, push_mem, pop_mem, overlap_i, pull_i = G.NonTerminals('<push> <pop> <push-mem> <pop-mem> <overlap> <pull>')


        dirx, idx, squarex, numx = G.Terminals('DIR ID SQUARE NUMBER')
        semi, comma, obrac, cbrac, okey, ckey, colon = G.Terminals('; , [ ] { } :')
        
        mov, copy, paste, mapx = G.Terminals('mov copy paste map')
        add, sub, mul, div, mod = G.Terminals('add sub mul div mod')
        goto, label = G.Terminals('goto label')
        push, pop, mem, overlap, pull = G.Terminals('push pop mem overlap pull')

        


        

        ########################################################
        # ==================================================== #
        ########################################################