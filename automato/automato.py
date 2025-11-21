from automato.passo import Passo

class Automato:
    def __init__(self,):
        self.estados = set()
        self.alfabeto = set()
        self.alfabetoPilha = set()
        self.transicoes = {}
        self.estadoInicial = None
        self.estadosFinais = set()
        self.pilha = []
        self.fita = ""
        self.posicaoFita = 0
        self.indicePasso = 0
        self.estadoAtual = None
        self.passos = []
        self.RESERVADOS = ['?', 'ε']
    
    def resetar(self):
        self.estadoAtual = self.estadoInicial
        self.pilha = []
        self.passos = []
        self.posicaoFita = 0
        self.indicePasso = 0
        self.passos.append(Passo(self.estadoAtual, self.posicaoFita, self.pilha, None))

    def inserirEstados(self, *estados):
        for estado in estados:
            self.estados.add(estado)       
    
    def removerEstados(self, *estados):
        for estado in estados:
            if estado not in self.estados:
                raise ValueError(f"Estado inválido: {estado}")
            
            transicoesRemover = []
            for chave, valor in self.transicoes.items():
                estadoOrigem = chave[0]
                estadoDestino = valor[0]

                if estadoOrigem == estado or estadoDestino == estado:
                    transicoesRemover.append(chave)
            
            for chave in transicoesRemover:
                self.removerTransicao(*chave)

            if estado in self.estadosFinais:
                self.estadosFinais.remove(estado)
            if self.estadoInicial == estado:
                self.estadoInicial = None
            self.estados.remove(estado)
    
    def inserirEstadoInicial(self, estado):
        self.estadoInicial = estado
        if estado not in self.estados:
            self.estados.add(estado)
    
    def removerEstadoInicial(self):
        self.estadoInicial = None

    def inserirEstadosFinais(self, *estados):
        for estado in estados:
            if estado not in self.estados:
                self.estados.add(estado)
            self.estadosFinais.add(estado)

    # Apenas remove como sendo um Estado Final, o estado continua existindo
    def removerEstadosFinais(self, *estados):
        for estado in estados:
            if estado in self.estadosFinais:
                self.estadosFinais.remove(estado)
            else:
                raise ValueError(f"Estado inexistente: {estado}")
    
    def inserirAlfabeto(self, *simbolos):
        for simbolo in simbolos:
            if simbolo in self.RESERVADOS:
                raise ValueError(f"Símbolo reservado: {simbolo}")
            self.alfabeto.add(simbolo)

    def removerAlfabeto(self, *simbolos):
        for simbolo in simbolos:
            if simbolo in self.alfabeto:
                self.alfabeto.remove(simbolo)
            else:
                raise ValueError(f"Símbolo não pertence ao alfabeto: {simbolo}")

    def inserirAlfabetoPilha(self, *simbolos):
        for simbolo in simbolos:
            if simbolo in self.RESERVADOS:
                raise ValueError(f"Símbolo reservado: {simbolo}")
            self.alfabetoPilha.add(simbolo)

    def removerAlfabetoPilha(self, *simbolos):
        for simbolo in simbolos:
            if simbolo in self.alfabetoPilha:
                self.alfabetoPilha.remove(simbolo)
            else:
                raise ValueError(f"Símbolo não pertence ao alfabeto da pilha: {simbolo}")


    def inserirTransicao(self, estadoOrigem, lidoFita, lidoPilha, novoEstado, palavraGravadaPilha):
        # verificar se estados existem
        # verificar se símbolo fita existe 
        # verificar se símbolo pilha existe

        if estadoOrigem not in self.estados or novoEstado not in self.estados:
            raise ValueError("Estado origem ou destino não existe")
        if lidoFita not in self.alfabeto and lidoFita not in self.RESERVADOS:
            raise ValueError(f"Símbolo {lidoFita} não pertence ao alfabeto")
        if lidoPilha not in self.alfabetoPilha and lidoPilha not in self.RESERVADOS:
            raise ValueError(f"Símbolo {lidoPilha} não pertence ao alfabeto de pilha")

        # verificar se a informação a ser inserida na pilha é válida. Símbolos reservados só podem ocorrer se a palavra for 1 caractere
        if len(palavraGravadaPilha) > 1:
            for simbolo in palavraGravadaPilha:
                if simbolo not in self.alfabetoPilha or simbolo in self.RESERVADOS:
                    raise ValueError(f"Símbolo {simbolo} não pertence ao alfabeto da pilha")
        elif palavraGravadaPilha not in self.alfabetoPilha and palavraGravadaPilha not in self.RESERVADOS:
            raise ValueError(f"Símbolo {palavraGravadaPilha} não pertence ao alfabeto da pilha")

            
        chave = (estadoOrigem, lidoFita, lidoPilha)

        # verificar o determinismo: o ε não permite inserção de qualquer outro simbolo. Inserção do símbolo ε só é perminitda se 
        # for a primeira transição para dada combinação de estado E topo da pilha. 
        # Diferentemente, o ? não quebra o determinismo
        for (estadoExistente, simboloExistente, pilhaExistente) in self.transicoes.keys():
            if estadoExistente != estadoOrigem:
                continue
            
            if simboloExistente == lidoFita and pilhaExistente == lidoPilha:               
                    raise ValueError("Transição duplicada")

            # Se existe uma transição que não lê nada na fita e na pilha, não pode exisitir outra transição para o mesmo estado 
            # pois causará, necessariamente, conflito não determinístico.
            # De maneira semelhante, se, para um mesmo estado, o ε aparecer em símbolo da fita e, apesar de ser em outra transição, 
            # aparecer em símbolo lido da pilha, ocorre não determinismo.
            if pilhaExistente == lidoPilha or pilhaExistente == 'ε' or lidoPilha == 'ε':   
                if lidoFita == 'ε' or simboloExistente == 'ε':
                    raise ValueError("Conflito não deterministico por conta do ε")
                    
            if simboloExistente == lidoFita or simboloExistente == 'ε' or lidoFita == 'ε':
                if lidoPilha == 'ε' or pilhaExistente == 'ε':
                    raise ValueError("Conflito não deterministico por conta do ε")
            
            
                
        self.transicoes[chave] = (novoEstado, palavraGravadaPilha)


    def obterTransicao(self, lidoFita, lidoPilha):
        return self.transicoes.get((self.estadoAtual, lidoFita, lidoPilha))         # retorna None se a chave não existir 
    
    def removerTransicao(self, estadoOrgigem, lidoFita, lidoPilha):
        chave = (estadoOrgigem, lidoFita, lidoPilha)
        if chave in self.transicoes:
            del self.transicoes[chave]
        else:
            raise ValueError("Chave inexistente")
        
    
    # faz todos os passos e armazena na lista
    def calcularPassos(self, palavra):
        self.fita = palavra
        self.resetar()
        contador = 0

        while (True):
            # Verificar loop infinito de maneira simples
            contador += 1
            if contador > 10000:
                return "REJEITA"

            if self.fitaVazia():
                opcoesFita = ['ε', '?']
            else:
                opcoesFita = [self.fita[self.posicaoFita], 'ε']
            if self.pilhaVazia():
                opcoesPilha = ['ε', '?']
            else:
                opcoesPilha = [self.pilha[-1], 'ε']

            entrou = False
            for f in opcoesFita:
                for p in opcoesPilha:
                    if self.obterTransicao(f, p) != None:
                        simbolo = f
                        simboloPilha = p
                        entrou = True
                        break
                if entrou:
                    break
            
            if entrou == False:
                if self.estadoAtual in self.estadosFinais and self.fitaVazia() == True:
                    return "ACEITA"
                return "REJEITA"

            if simbolo not in self.RESERVADOS:
                self.posicaoFita += 1
            if simboloPilha not in self.RESERVADOS:
                self.pilha.pop()


            chave = (self.estadoAtual, simbolo, simboloPilha)
            transicao = self.obterTransicao(simbolo, simboloPilha)

            self.estadoAtual = transicao[0]

            if len(transicao[1]) > 1:
                for s in transicao[1]:
                    self.pilha.append(s)
            elif transicao[1] not in self.RESERVADOS:
                self.pilha.append(transicao[1])
            
            transicaoUsada = ([chave] + [transicao])

            self.passos.append(Passo(self.estadoAtual, self.posicaoFita, self.pilha, transicaoUsada))
    
 
    def proximoPasso(self):
        if self.indicePasso + 1 == len(self.passos):
            raise ValueError("Simulação está no passo final")
        self.indicePasso += 1
        return self.passos[self.indicePasso]
    
    def passoAnterior(self):
        if self.indicePasso == 0:
            raise ValueError("Simulação está no primeiro passo")
        self.indicePasso -= 1
        return self.passos[self.indicePasso]
    
    def passoAtual(self):
        return self.passos[self.indicePasso]
    
    def pilhaVazia(self):
        if len(self.pilha) == 0:
            return True
        return False
    
    def fitaVazia(self):
        if self.posicaoFita >= len(self.fita):
            return True
        return False