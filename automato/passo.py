class Passo:
    def __init__(self, estadoAtual, posicaoFita, pilha, transicaoUsada):
        self.estadoAtual = estadoAtual
        self.posicaoFita = posicaoFita
        self.pilha = pilha[:]
        self.transicaoUsada = transicaoUsada