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
    