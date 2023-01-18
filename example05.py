from tools.shift_reduce import LR1Parser, evaluate_reverse_parse
from tools.lexer import Lexer
from tools.pycompiler import Grammar, Terminal, NonTerminal, Token
from tools.ast import Node
from utils05.utils import Scope
import tools.visitor as visitor

##################################
class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements
        
class StatementNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

#################################

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body

class PrintNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

####################################

class ConstantNumNode(AtomicNode):
    def evaluate(self):        
        return float(self.lex)

class VariableNode(AtomicNode):
    def evaluate(self):
        return float(self.lex)

class CallNode(AtomicNode):
    def __init__(self, idx, args):
        AtomicNode.__init__(self, idx)
        self.args = args

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

##################################

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'
    
    @visitor.when(PrintNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PrintNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CallNode: {node.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'


########################################################
#                 CHEQUEO SEMANTICO 1                  #        
########################################################
class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        # Your code here!!!
        scope = Scope()
        for st in node.statements:
            st : StatementNode
            self.visit(st, scope)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        # Your code here!!!        
        if scope.is_var_defined(node.id):
            self.errors.append(f'La variable {node.id} ya ha sido definida previamente.')
        else:
            scope.define_variable(node.id)
            self.visit(node.expr, scope)
        
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        # Your code here!!!
        if scope.is_func_defined(node.id, len(node.params)):
            self.errors.append(f"La funcion '{node.id} ({node.params})' ya esta definida.")
        else:
            scope.define_function(node.id, node.params)
            child = scope.create_child_scope()
            self.visit(node.body, child)
                
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        # Your code here!!!
        self.visit(node.expr, scope)
        
    
    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):
        # Your code here!!!
        try:
            value = float(node.lex)
            node.lex = value
        except:
            self.errors.append('No se puede convertir a float')
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        # Your code here!!!
        if not scope.is_var_defined(node.lex):
            self.errors.append(f'La variable {node.lex} no ha sido definida.')          
    
    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        # Your code here!!!
        if not scope.is_func_defined(node.lex, len(node.args)):
            self.errors.append(f'La funcion {node.lex} no ha sido definida')        
        for arg in node.args:
            arg: ExpressionNode
            self.visit(arg, scope)
        
    
    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope: Scope):
        # Your code here!!!   
        self.visit(node.left, scope)
        self.visit(node.right, scope)   


class Language05:
    def __init__(self) -> None:
        ########################################################
        #                 GRAMATICA 05  LR(1)                  #        
        ########################################################
        G = Grammar()

        program = G.NonTerminal('<program>', startSymbol=True)
        stat_list, stat = G.NonTerminals('<stat_list> <stat>')
        let_var, def_func, print_stat, arg_list = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list>')
        expr, term, factor, atom = G.NonTerminals('<expr> <term> <factor> <atom>')
        func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')

        let, defx, printx = G.Terminals('let def print')
        semi, comma, opar, cpar, arrow = G.Terminals('; , ( ) ->')
        equal, plus, minus, star, div = G.Terminals('= + - * /')
        idx, num = G.Terminals('id int')

        program %= stat_list, lambda h,s: ProgramNode(s[1])

        stat_list %= stat + semi, lambda h,s: [s[1]]  
        stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3]  

        stat %= let_var, lambda h,s: s[1]  
        stat %= def_func, lambda h,s: s[1]  
        stat %= print_stat, lambda h,s: s[1]  

        let_var %= let + idx + equal + expr, lambda h,s: VarDeclarationNode(s[2], s[4])  

        def_func %= defx + idx + opar + arg_list + cpar + arrow + expr, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7])  

        print_stat %= printx + expr, lambda h,s: PrintNode(s[2])  

        arg_list %= idx, lambda h, s: [s[1]]
        arg_list %= idx + comma + arg_list, lambda h, s: [s[1]] + s[3]

        expr %= expr + plus + term, lambda h,s: PlusNode(s[1], s[3])  
        expr %= expr + minus + term, lambda h,s: MinusNode(s[1], s[3])  
        expr %= term, lambda h,s: s[1]  

        term %= term + star + factor, lambda h,s:  StarNode(s[1], s[3])  
        term %= term + div + factor, lambda h,s: DivNode(s[1], s[3])  
        term %= factor, lambda h,s: s[1]  

        factor %= atom, lambda h,s: s[1]  
        factor %= opar + expr + cpar, lambda h,s: s[2]  

        atom %= num, lambda h,s: ConstantNumNode(s[1])  
        atom %= idx, lambda h,s: VariableNode(s[1])  
        atom %= func_call, lambda h,s: s[1]  

        func_call %= idx + opar + expr_list + cpar, lambda h, s: CallNode(s[1], s[3])

        expr_list %= expr, lambda h,s: [s[1]]
        expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3]  
        
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

                (arrow, '->'),

                (semi, ';'),
                (comma, ','),
                (equal, '='),

                (let, 'let'),
                (printx, 'print'),
                (defx, 'def'),

                (opar, '\('),
                (cpar, '\)'),

                (idx, '(a|b|x|y|f|F|Y|X)(a|b|x|y|f|F|Y|X)*'),
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
        self.formatter = FormatVisitor()
    
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
        print(self.formatter.visit(ast))
