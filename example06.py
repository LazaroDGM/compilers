from tools.shift_reduce import LR1Parser, evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token

class Language06:
    def __init__(self) -> None:
        ########################################################
        #                GRAMATICA 06  SLR(1)                  #        
        ########################################################

        G = Grammar()

        program = G.NonTerminal('<program>', startSymbol=True)
        stat_list, stat = G.NonTerminals('<stat_list> <stat>')
        let_var, def_func, param_list, let_const = G.NonTerminals('<let-var> <def-func> <arg-list> <let-const>')
        expr, term, factor, atom = G.NonTerminals('<expr> <term> <factor> <atom>')
        func_call, arg_list, arg = G.NonTerminals('<func-call> <param-list> <param>')
        if_stat, while_stat, asign_stat, return_stat = G.NonTerminals('<if-stat> <while-stat> <asign-stat> <return-const>')
        param, comp_list, comp = G.NonTerminals('<arg> <comp-list> <comp>')

        var, func, const, returnx = G.Terminals('var func const return')
        semi, comma, opar, cpar, arrow, okey, ckey, colon = G.Terminals('; , ( ) -> { } :')
        asign, plus, minus, star, div = G.Terminals('= + - * /')
        andx, orx = G.Terminals('&& ||')
        eq, neq, lte, gte, lt, gt = G.Terminals('== != <= >= < >')

        ifx, elsex, endif, whilex, endwhile = G.Terminals('if else endif while endwhile')
        idx, num, boolx, typex = G.Terminals('ID NUMBER BOOL TYPE')


        program %= stat_list

        stat_list %= stat + semi
        stat_list %= stat + semi + stat_list

        stat %= let_var
        stat %= let_const
        stat %= if_stat
        stat %= while_stat
        stat %= asign_stat
        stat %= def_func
        stat %= return_stat       

        let_var %= var + typex + idx + asign + arg
        let_var %= var + typex + idx

        let_const %= const + typex + idx + asign + arg

        asign_stat %= idx + asign + arg

        def_func %= func + idx + opar + param_list + cpar + arrow + typex + okey + stat_list + ckey
        def_func %= func + idx + opar + param_list + cpar + okey + stat_list + ckey

        return_stat %= returnx + arg

        if_stat %= ifx + opar + comp_list + cpar + colon + stat_list + endif
        if_stat %= ifx + opar + comp_list + cpar + colon + stat_list + elsex + stat_list + endif

        while_stat %= whilex + opar + comp_list + cpar + colon + stat_list + endwhile

        param_list %= param
        param_list %= param + comma + param_list

        param %= typex + idx

        comp_list %= comp_list + andx + comp
        comp_list %= comp_list + orx + comp
        comp_list %= comp
        #cond_list %= expr

        comp %= expr + eq + expr
        comp %= expr + neq+ expr
        comp %= expr + lte + expr
        comp %= expr + gte + expr
        comp %= expr + lt + expr
        comp %= expr + gt + expr
        comp %= expr        

        expr %= expr + plus + term
        expr %= expr + minus + term
        expr %= term

        term %= term + star + factor
        term %= term + div + factor
        term %= factor

        factor %= atom
        
        factor %= opar + comp_list + cpar

        atom %= num
        atom %= idx
        atom %= boolx
        atom %= func_call

        func_call %= idx + opar + arg_list + cpar
        func_call %= idx + opar + cpar

        arg_list %= arg + comma + arg_list
        arg_list %= arg
        
        arg %= comp_list

        nonzero_digits = '|'.join(str(n) for n in range(1,10))
        letters_lower = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
        letters_power = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))

        ########################################################
        # ==================================================== #
        ########################################################


        ########################################################
        #                        LEXER                         #
        ########################################################
        lexer = Lexer(
            [
                ('space', '( |\t|\n)( |\t|\n)*'),

                (var,'var'),
                (const,'const'),
                (func,'func'),
                (ifx,'if'),
                (endif,'endif'),
                (elsex,'else'),
                (whilex,'while'),
                (endwhile,'endwhile'),
                (returnx, 'return'),    

                (comma, ','),
                (semi,';'),
                (asign,'='),
                (arrow,'->'),
                (okey, '{'),
                (ckey, '}'),
                (opar, '\('),
                (cpar,'\)'),
                (colon,':'),

                (plus,'\+'),
                (minus,'-'),
                (star, '\*'),
                (div, '/'),

                (andx, '&&'),
                (orx, '\|\|'),

                (eq,'=='),
                (neq,'!='),
                (lte,'<='),
                (gte,'>='),
                (lt,'<'),
                (gt,'>'),

                (boolx, '(True)|(False)'),
                (num,f'({nonzero_digits})(0|{nonzero_digits})*'),
                (typex, '(int)|(bool)'),
                (idx, f'({letters_lower}|{letters_power})({letters_lower}|{letters_power})*')

            ],
            G.EOF
        )

        self.lexer = lexer
        ########################################################
        #                    PARSER SLR(1)                     #
        ########################################################
        parser = SLR1Parser(G)
        self.parser = parser

    ####################################
    #              VALID               #
    ####################################
    def is_Valid(self, text, verbose=False):
        all_tokens = self.lexer(text)
        tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
        right_parse, operations = self.parser(tokens)  
        return True 

L = Language06()