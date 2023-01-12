from pycompiler import ContainerSet, Grammar

def compute_local_first(firsts: dict, alpha):
    '''
    Calcula los firsts de la forma oracional `alpha`, para un conjunto de first actuales

    Parametros
    -----------
        `firsts`: Diccionario de formas oracaionales y firsts
        `alpha`: Forma oracional

    Retorna
    -----------
        `first_alpha`: El conjunto de no terminales obtenidos, dentro de un `ContainerSet`
    '''
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
    elif alpha[0].IsTerminal:
        first_alpha.add(alpha[0])
    elif alpha[0].IsNonTerminal:
        if len(alpha) > 1:
            first_alpha.update(firsts[alpha[0]])
        else:
            first_alpha.hard_update(firsts[alpha[0]])
        #if len(alpha) > 1 and alpha[0].IsEpsilon:
        if firsts[alpha[0]].contains_epsilon and len(alpha) > 1:            
            Z = alpha[1:]
            first_alpha.hard_update(compute_local_first(firsts,Z))
        
    return first_alpha

def compute_firsts(G: Grammar):
    '''
    Calcula el First de todas las formas oracionales de la gramatica `G`

    Parametros
    ----------
        `G`: La gramatica a la que se le hallara el conjunto First. Debe ser `Grammar`
    '''
    firsts = {}
    change = True
        
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
                
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
                        
            local_first = compute_local_first(firsts, alpha)            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts

def compute_follows(G, firsts):
    '''
    Funcion para calcular el Follow de todos los No-Terminales de la gramatica `G`
    dado el conjunto de todos los Firsts

    Parametros
    -------------
        `G`: La gramatica a la que se le hallara los conjuntos Follows. Debe ser `Grammar`
        `firsts`: Diccionario de todos los Firsts de la gramatica
    '''
    follows = { }
    change = True
    
    #local_firsts = {}

    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]

            for i in range(0, len(alpha)):
                A = alpha[i]
                if A.IsNonTerminal:
                    firsts_Z = ContainerSet()
                    if i < len(alpha)-1:
                        firsts_Z = compute_local_first(firsts, alpha[i+1:])                    
                    change = change or follows[A].update(firsts_Z)
                    if firsts_Z.contains_epsilon or i == len(alpha)-1:
                        change = change or follows[A].update(follow_X)    
    return follows

