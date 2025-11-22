import graphviz

def gerarSvgAutomato(automato):
    dot = graphviz.Digraph()
    dot.attr(rankdir = 'LR')

    dot.node("", shape="none")
    dot.edge("", automato.estadoInicial)

    for estado in automato.estados:
        if estado in automato.estadosFinais:
            dot.node(estado, shape = 'doublecircle')
        else:
            dot.node(estado, shape = 'circle')

    for (estadoOrigem, simboloFita, simboloPilha), (estadoDestino, palavraGravadaPilha) in automato.transicoes.items():
        label = f"({simboloFita}, {simboloPilha}, {palavraGravadaPilha})"

        dot.edge(estadoOrigem, estadoDestino, label=label)
    
    return dot.pipe(format = 'svg').decode('utf-8')

def gerarSvgAutomatoDestacado(automato, passo):
    dot = graphviz.Digraph()
    dot.attr(rankdir = 'LR')

    dot.node("", shape="none")
    dot.edge("", automato.estadoInicial)

    for estado in automato.estados:
        if passo.estadoAtual == estado and passo.estadoAtual in automato.estadosFinais:
            dot.node(estado, shape = 'doublecircle', color = 'red')
            continue
        if passo.estadoAtual == estado:
            dot.node(estado, shape = 'circle', color = 'red')
            continue
        if estado in automato.estadosFinais:
            dot.node(estado, shape = 'doublecircle')
        else:
            dot.node(estado, shape = 'circle')

    for (estadoOrigem, simboloFita, simboloPilha), (estadoDestino, palavraGravadaPilha) in automato.transicoes.items():
        label = f"({simboloFita}, {simboloPilha}, {palavraGravadaPilha})"

        if [(estadoOrigem, simboloFita, simboloPilha), (estadoDestino, palavraGravadaPilha)] == passo.transicaoUsada:
            dot.edge(estadoOrigem, estadoDestino, label=label, color = 'red')
            continue

        dot.edge(estadoOrigem, estadoDestino, label=label)
    
    return dot.pipe(format = 'svg').decode('utf-8')