from tools.shift_reduce import LR1Parser, evaluate_reverse_parse, SLR1Parser, table_to_dataframe
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
from utils06.utils import AsignVarNode, AtomicNode, BinaryNode, CallNode, ConstantNumNode
from utils06.utils import ConstDeclarationNode, DivNode, ExpressionNode, FuncDeclarationNode
from utils06.utils import IfElseEndNode, IfEndNode, PlusNode, ProgramNode, ReturnNode, VarDeclarationNode
from utils06.utils import MinusNode, StarNode, DivNode, VariableNode, BoolNode
from utils06.utils import EqualNode, NotEqualNode, LessThanEqualNode, LessThanNode, GreaterEqualNode, GreaterNode
from utils06.utils import AndNode, OrNode, WhileNode, ParamNode, ParamListNode


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


        program %= stat_list, lambda h,s: ProgramNode(s[1])

        stat_list %= stat + semi, lambda h,s: s[1]
        stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3]

        stat %= let_var, lambda h,s: s[1]
        stat %= let_const, lambda h,s: s[1]
        stat %= if_stat, lambda h,s: s[1]
        stat %= while_stat, lambda h,s: s[1]
        stat %= asign_stat, lambda h,s: s[1]
        stat %= def_func, lambda h,s: s[1]
        stat %= return_stat, lambda h,s: s[1]

        let_var %= var + typex + idx + asign + arg, lambda h,s: VarDeclarationNode(idx= s[3], ttype=s[2], expr=s[5])
        let_var %= var + typex + idx, lambda h,s: VarDeclarationNode(idx= s[3], ttype=s[2], expr=None)

        let_const %= const + typex + idx + asign + arg, lambda h,s: ConstDeclarationNode(idx= s[3], ttype=s[2], expr=s[5])

        asign_stat %= idx + asign + arg, lambda h,s: AsignVarNode(idx= s[1], expr=s[3])

        def_func %= func + idx + opar + param_list + cpar + arrow + typex + okey + stat_list + ckey, \
            lambda h,s: FuncDeclarationNode(idx= s[2], params= s[4].ids, types= s[4].ttypes, return_type= s[7], body=s[9])
        def_func %= func + idx + opar + param_list + cpar + okey + stat_list + ckey, \
            lambda h,s: FuncDeclarationNode(idx= s[2], params= s[4].ids, types= s[4].ttypes, return_type= None, body=s[7])

        return_stat %= returnx + arg, lambda h,s: ReturnNode(s[2])

        if_stat %= ifx + opar + comp_list + cpar + colon + stat_list + endif, lambda h,s: IfEndNode(s[3], s[6])
        if_stat %= ifx + opar + comp_list + cpar + colon + stat_list + elsex + stat_list + endif, lambda h,s: IfElseEndNode(s[3], s[6], s[8])

        while_stat %= whilex + opar + comp_list + cpar + colon + stat_list + endwhile, lambda h,s: WhileNode(s[3], s[6])

        param_list %= param, lambda h,s: ParamListNode(idxs= [ s[1].id ], ttypes= [ s[1].ttype ])
        param_list %= param + comma + param_list, lambda h,s: ParamListNode(idxs= [ s[1].id ] + s[3].ids, ttypes= [ s[1].ttype ] + s[3].ttypes)

        param %= typex + idx, lambda h,s: ParamNode(idx= s[2], ttype= s[1])

        comp_list %= comp_list + andx + comp, lambda h,s: AndNode(s[1], s[3])
        comp_list %= comp_list + orx + comp, lambda h,s: OrNode(s[1], s[3])
        comp_list %= comp, lambda h,s: s[1]
        #cond_list %= expr

        comp %= expr + eq + expr, lambda h,s: EqualNode(s[1], s[3])
        comp %= expr + neq+ expr, lambda h,s: NotEqualNode(s[1], s[3])
        comp %= expr + lte + expr, lambda h,s: LessThanEqualNode(s[1], s[3])
        comp %= expr + gte + expr, lambda h,s: GreaterEqualNode(s[1], s[3])
        comp %= expr + lt + expr, lambda h,s: LessThanNode(s[1], s[3])
        comp %= expr + gt + expr, lambda h,s: GreaterNode(s[1], s[3])
        comp %= expr, lambda h,s: s[1]

        expr %= expr + plus + term, lambda h,s: PlusNode(left= s[1], right=s[3])
        expr %= expr + minus + term, lambda h,s: MinusNode(left= s[1], right=s[3])
        expr %= term, lambda h,s: s[1]

        term %= term + star + factor, lambda h,s: StarNode(left= s[1], right=s[3])
        term %= term + div + factor, lambda h,s: DivNode(left= s[1], right=s[3])
        term %= factor, lambda h,s: s[1]

        factor %= atom, lambda h,s: s[1]
        factor %= opar + comp_list + cpar, lambda h,s: s[2]

        atom %= num, lambda h,s: ConstantNumNode(s[1])
        atom %= idx, lambda h,s: VariableNode(s[1])
        atom %= boolx, lambda h,s: BoolNode(s[1])
        atom %= func_call, lambda h,s: s[1]

        func_call %= idx + opar + arg_list + cpar, lambda h,s: CallNode(idx= s[1], args= s[3])
        func_call %= idx + opar + cpar, lambda h,s: CallNode(idx= s[1], args=[])

        arg_list %= arg + comma + arg_list, lambda h,s: [ s[1] ] + s[3]
        arg_list %= arg, lambda h,s: [ s[1] ]
        
        arg %= comp_list, lambda h,s: s[1]

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