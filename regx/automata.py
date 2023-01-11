import sys

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):        
        if symbol not in self.vocabulary:
            print(f"El simbolo: '{symbol}', no pertenece al vocabulario del automata.", file=sys.stderr)
            return False
        current_transitions = self.transitions[self.current]
        if symbol in current_transitions.keys():
            self.current = self.transitions[self.current][symbol][0]
            return True
        print(f"No hay transicion desde el estado '{self.current}' " + \
                f" para el simbolo: '{symbol}'")
        return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):        
        self._reset()
        for i in string:
            if not self._move(i):
                return False
        if self.current in self.finals:
            return True
        return False
