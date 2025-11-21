from automato.automato import Automato

def casosTeste():
    # Caso de teste simples
    automato = Automato()
    automato.inserirEstados('q0', 'q1', 'qf', 'q2')
    automato.inserirEstadoInicial('q0')
    automato.inserirEstadosFinais('qf')
    automato.inserirAlfabeto('a', 'b')
    automato.inserirAlfabetoPilha('X', 'Z')

    automato.inserirTransicao('q0', 'a', 'ε', 'q1', 'X') 
    automato.inserirTransicao('q1', 'b', 'X', 'q0', 'ε') 
    automato.inserirTransicao('q1', '?', 'ε', 'qf', 'ε') 


    # Casos de não determinismo
    # 1:
    #automato.inserirTransicao('q2', 'ε', 'X', 'q0', 'X')
    #automato.inserirTransicao('q2', 'a', 'X', 'q0', 'ε')

    # 2:
    #automato.inserirTransicao('q2', 'b', 'X', 'q0', 'X')
    #automato.inserirTransicao('q2', 'b', 'ε', 'q0', 'ε')

    # 3:
    #automato.inserirTransicao('q2', 'b', 'X', 'q0', 'X')
    #automato.inserirTransicao('q2', 'ε', 'ε', 'q0', 'ε')

    # 4:
    #automato.inserirTransicao('q2', 'b', 'ε', 'q0', 'X')
    #automato.inserirTransicao('q2', 'ε', 'X', 'q0', 'ε')

    resultado = automato.calcularPassos("ababa")
    print(f"\nResultado para 'ababa': {resultado}")

    resultado = automato.calcularPassos("ababaa")
    print(f"\nResultado para 'ababaa': {resultado}")


def terminal(): 
    automato = Automato()
    while(True):
        print("Opções: ")
        print("1 - Inserir Estados")
        print("2 - Inserir Alfabeto Principal")
        print("3 - Inserir Alfabeto Pilha")
        print("4 - Inserir Transições")
        print("5 - Simular")
        print("6 - Casos de teste")
        print("7 - Remover")
        print("0 - Sair")
        resposta = input("Resposta: ")

        if resposta == '1':
            estados = []
            finais = []
            
            estados = input("Digite os estados separados por espaço: ").split()
            automato.inserirEstados(*estados)

            inicial = input("Digite o estado inicial: ")
            automato.inserirEstadoInicial(inicial)

            finais = input("Digite os estados finais separados por espaço: ").split()
            automato.inserirEstadosFinais(*finais)

        elif resposta == '2':
            alfabeto = []
            while True:
                try:
                    alfabeto = input("Digite os símbolos do alfabeto principal separados por espaço: ").split()
                    automato.inserirAlfabeto(*alfabeto)
                    break
                except ValueError as e:
                    print(e)
            
        elif resposta == '3':
            alfabeto = []
            while True:
                try:
                    alfabeto = input("Digite os símbolos do alfabeto da pilha separados por espaço: ").split()
                    automato.inserirAlfabetoPilha(*alfabeto)
                    break
                except ValueError as e:
                    print(e)

        elif resposta == '4':
            while True:
                estadoOrigem = input("Informe o estado de origem: ")
                lerFita = input("Informe o símbolo a ser lido da fita: ")
                lerPilha = input("Informe o símbolo a ser lido da pilha: ")
                estadoDestino = input("Informe o estado destino: ")
                PalavraGravadaPilha = input("Informe a palavra a ser escrita na pilha: ")

                try:
                    automato.inserirTransicao(estadoOrigem, lerFita, lerPilha, estadoDestino, PalavraGravadaPilha)
                except ValueError as e:
                    print(e)

                resposta = input("Deseja continuar? ")
                if resposta.lower() not in ("sim", 's'):
                    break

        elif resposta == '5':
            palavra = input("Informe a palavra: ")
            feedback = automato.calcularPassos(palavra)
            while True:
                print("1 - Avançar")
                print("2 - Retroceder")
                print("3 - Atual")
                print("4 - Feedback")
                print("0 - Sair")
                resposta = input("Resposta: ")

                if resposta == '1':
                    try:
                        passo = automato.proximoPasso()
                        print(passo.estadoAtual)
                        print(passo.posicaoFita)
                        print(passo.pilha)
                        print(passo.transicaoUsada)
                    except ValueError as e:
                        print(e)

                elif resposta == '2':
                    try:
                        passo = automato.passoAnterior()
                        print(passo.estadoAtual)
                        print(passo.posicaoFita)
                        print(passo.pilha)
                        print(passo.transicaoUsada)
                    except ValueError as e:
                        print(e)

                elif resposta == '3':
                    passo = automato.passoAtual()
                    print(passo.estadoAtual)
                    print(passo.posicaoFita)
                    print(passo.pilha)
                    print(passo.transicaoUsada)

                elif resposta == '4':
                    print(feedback)
                elif resposta == '0':
                    break
                else:
                    print("Opção inválida")

        elif resposta == '6':
            casosTeste()
        
        elif resposta == '7':
            estado = input("Estado a remover: ").split()
            print("Antes: ")
            print(automato.transicoes)
            print(automato.estadoInicial)
            print(automato.estadosFinais)
            print(automato.estados)
            automato.removerEstados(*estado)
            print("Depois: ")
            print(automato.transicoes)
            print(automato.estadoInicial)
            print(automato.estadosFinais)
            print(automato.estados)
        elif resposta == '0':
            return 
        else:
            print("Opção inválida")


if __name__ == "__main__":
    terminal()