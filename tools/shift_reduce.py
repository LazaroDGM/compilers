from automata import State
from pycompiler import Grammar, Item, ContainerSet
from parserLL1 import compute_first_follows, compute_firsts, compute_follows, compute_local_first

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
    
    def __init__(self, G: Grammar, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value

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

class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state                

                if not item.IsReduceItem:
                    symbol =  item.NextSymbol
                    if symbol.IsTerminal:                        
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata No Determinista.'
                            self._register(self.action,
                                        (idx, item.NextSymbol.Name),
                                        (ShiftReduceParser.SHIFT, node_transition[0].idx))
                    else:
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata no determinista.'
                            self._register(self.goto,
                                        (idx, item.NextSymbol.Name),
                                        (node_transition[0].idx))                    
                else:
                    left, right = production = item.production
                    k = G.Productions.index(production)
                    if left.Name == G.startSymbol.Name:
                        k = G.Productions.index(item.production)
                        self._register(self.action,
                            (idx, G.EOF.Name),
                            (ShiftReduceParser.OK, k))                    
                    for terminal in follows[left]:
                        ################TODO##############
                        # Mejorar la actualizacion de OK #
                        ##################################
                        if terminal == G.EOF and left.Name == G.startSymbol.Name:
                            continue
                        self._register(self.action,
                                    (idx, terminal.Name),
                                    (ShiftReduceParser.REDUCE, k))

def expand(item, firsts):
    '''
    Esta recibe un item LR(1) y devuelve el conjunto de items
    que sugiere incluir (directamente) debido a la presencia de un `.`
    delante de un no terminal.
    
    Parametros
    --------------
        `item`: Item LR(1) a expandir
        `firsts`: El conjunto de firsts

    Retorna:
    --------------
        `lookaheads`: El conjunto de las producciones sugeridas,
        con los lookaheads que pertenecen al Firsts del resto de la
        formal oracional y su lookahead actual
    '''
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
     
    for preview in item.Preview():
        local_firsts= compute_local_first(firsts, preview)
        for production in next_symbol.productions:
            new_item = Item(production, 0, local_firsts)
            lookaheads.add(new_item)
    
    assert not lookaheads.contains_epsilon
    
    return list(lookaheads)

