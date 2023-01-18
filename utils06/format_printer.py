try:
    from utils import *
except:
    from utils06.utils import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: var {node.ttype} {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(ConstDeclarationNode)
    def visit(self, node: ConstDeclarationNode, tabs=0):
        ans = '\t' * tabs + f'\\__ConstDeclarationNode: var {node.ttype} {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode, tabs=0):
        ans = '\t' * tabs + f'\\__ReturnNode: return <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, tabs=0):
        params = ', '.join([str(ttype) + ' '+ str(idx) for ttype, idx in zip(node.types, node.params)])
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> {node.return_type} <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
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