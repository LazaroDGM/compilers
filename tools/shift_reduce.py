from automata import State
from pycompiler import Grammar, Item
from parserLL1 import compute_first_follows, compute_firsts, compute_follows

def build_LR0_automaton(G: Grammar):
    '''
    Construye un automata LR0 a partir de una gramatica. El automata creado
    con esta funcion es la version No Determinista. Se recomienda hacerle
    la transformacion a un DFA para su uso. La gramatica debe estar aumentada,
    si el distinguido tiene varias producciones.

    Parametros:
    --------------
        `G`: Gramatica a la que se le quiere construir el automata. Debe ser instancia de `Grammar`,
        y ser una gramatica aumentada.
    '''
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
                
        kernel = Item(current_item.production, current_item.pos + 1)
        kernel_state = State(kernel, True)
        visited[kernel] = kernel_state

        next_symbol = current_item.NextSymbol
        no_kernels = []
        if next_symbol.IsNonTerminal:
            for production in next_symbol.productions:
                no_kernel = Item(production, 0)
                if no_kernel not in visited.keys():
                    visited[no_kernel] = State(no_kernel, True)
                    pending.append(no_kernel)
                no_kernels.append(no_kernel)
        
        current_state = visited[current_item]        
                
        current_state.add_transition(next_symbol.Name, visited[kernel])
        pending.append(kernel)
        for no_kernel in no_kernels:
            current_state.add_epsilon_transition(visited[no_kernel])            

    return automaton

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        count= 1
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:], count)
            count+=1
                            
            lookahead = lookahead.Name
            if (state, lookahead) not in self.action.keys():
                ##########################TODO###########################
                # Mejorar la informacion al detectar error en la cadena #
                #########################################################
                raise Exception(f'No se puede parsear la cadena. No se esperaba un token {lookahead}')
            
            action, tag = self.action[state, lookahead]
            
            # SHIFT
            if action == ShiftReduceParser.SHIFT:
                stack.append(lookahead)
                stack.append(tag)
                cursor += 1

            # REDUCE
            elif action == ShiftReduceParser.REDUCE:
                left, right = production = self.G.Productions[tag]
                count_delete = 2 * len(right)
                for i in range(count_delete):
                    stack.pop()
                new_state = self.goto[stack[-1], left.Name]
                stack.append(left.Name)
                stack.append(new_state)
                output.append(production)

            # ACCEPT
            elif action == ShiftReduceParser.OK:
                return output

            # INVALID 
            else:
                raise Exception('Invalid')
