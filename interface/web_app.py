from nicegui import ui
from interface.grafos import gerarSvgAutomato
from interface.grafos import gerarSvgAutomatoDestacado
from automato.automato import Automato
import re
import copy


automato = Automato()

automato.inserirEstados('q0', 'q1', 'qf')
automato.inserirEstadoInicial('q0')
automato.inserirEstadosFinais('qf')
automato.inserirAlfabeto('a', 'b')
automato.inserirAlfabetoPilha('X', 'Z')

automato.inserirTransicao('q0', 'a', 'ε', 'q1', 'X') 
automato.inserirTransicao('q1', 'b', 'X', 'q0', 'ε') 
automato.inserirTransicao('q1', '?', 'ε', 'qf', 'ε') 


#automato.inserirEstados('q0', 'qf')

#automato.inserirEstadoInicial('q0')
#automato.inserirEstadosFinais('qf')

#automato.inserirAlfabeto('a', 'b', 'c', 'd')
#automato.inserirAlfabetoPilha('A', 'Z')

#automato.inserirTransicao('q0', 'a', 'ε', 'q0', 'A')
#automato.inserirTransicao('q0', 'b', 'ε', 'q0', 'Z')
#automato.inserirTransicao('q0', 'c', 'Z', 'q0', 'ε')
#automato.inserirTransicao('q0', 'd', 'A', 'q0', 'ε')
#automato.inserirTransicao('q0', '?', '?', 'qf', 'ε')



def gerar(grafo):
        svg = gerarSvgAutomato(automato)
        grafo.set_content(svg)

@ui.page('/')
def index():

    def gerarAutomato():
        global automato
        # preciso aplicar rollback manual :D
        print(f"estados = {automato.estados}")
        try:
            # Impede do automato antigo ser receber alterações inválidas em caso de erro
            # Se quiser que as informações antigas importem, o tempo precisa ser copia do principal.
            automatoTemp = Automato()

            if i_estadoInicial.error:
                raise ValueError("Apenas 1 estado inicial é permitido")
        
            estadoInicial = i_estadoInicial.value

            t = i_transicoes.value
            pattern = r"""^(?:\(\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*\))(?:\s*,\s*\(\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*,\s*[^,()]+\s*\))*$"""

            if not re.match(pattern, t, re.VERBOSE):
                ui.notify("transição inválida")
                return
            listaTransicoes = [tuple(x.strip() for x in group.split(",")) 
            for group in re.findall(r"\((.*?)\)", t)]
            print(listaTransicoes)


            # inserir estados
            estados = [e.strip() for e in i_estados.value.split(',')]
            print(estados)
            automatoTemp.inserirEstados(*estados)

            #inserir estado inicial
            print(estadoInicial)
            automatoTemp.inserirEstadoInicial(estadoInicial)

            #inserir estados finais
            estadosFinais = [e.strip() for e in i_estadosFinais.value.split(',')]
            print(estadosFinais)
            automatoTemp.inserirEstadosFinais(*estadosFinais)


            #inserir alfabeto fita
            alfabetofita = [s.strip() for s in i_alfabetoFita.value.split(',')]
            print(alfabetofita)
            automatoTemp.inserirAlfabeto(*alfabetofita)

            #inserir alfabeto pilha
            alfabetoPilha = [s.strip() for s in i_alfabetoPilha.value.split(',')]
            print(alfabetoPilha)
            automatoTemp.inserirAlfabetoPilha(*alfabetoPilha)

            #inserir transicoes
            for transicao in listaTransicoes:
                estadoOrigem = transicao[0]
                simboloFita = transicao[1]
                simboloPilha = transicao[2]
                estadoDestino = transicao[3]
                palavraGravadaPilha = transicao[4]

                automatoTemp.inserirTransicao(estadoOrigem, simboloFita, simboloPilha, estadoDestino, palavraGravadaPilha)      
            
            # Por consequência, o automato antigo deixa de existir ao chamar essa função. 
            # Tecnicamente é o resultado que quero apesar de não ser elegante.
            # Mudanças dinâmicas e reutilizar o objeto aumenta muito a complexidade.
            automato = copy.deepcopy(automatoTemp)


            print(f"estados = {automato.estados}")
            ui.navigate.to('/automato')
        except ValueError as e:
            ui.notify(e)

    with ui.grid(columns=2).classes('items-center'):
        ui.label("Estados")
        i_estados = ui.input("Separados por vírgula")

        ui.label("Estado inicial:")
        i_estadoInicial = ui.input('Apenas 1', validation={
        'Não pode conter vírgula': lambda v: ',' not in v,
        'Máximo 10 caracteres': lambda v: len(v) <= 10,
        }).classes('w-64')

        ui.label("Estados finais:")
        i_estadosFinais = ui.input("Separados por vírgula").classes('w-64')

        ui.label("Alfabeto Fita: ")
        i_alfabetoFita = ui.input("Separados por vírgula").classes('w-64')

        ui.label("Alfabeto Pilha: ")
        i_alfabetoPilha = ui.input("Separados por vírgula").classes('w-64')

        ui.label("Transições: ")
        i_transicoes = ui.input("(Origem, Fita, Pilha, Destino, Empilha), (Origem, Fita, Pilha, Destino, Empilha)")


    ui.space().classes("h-16")

    ui.button("Gerar Autômato", on_click=gerarAutomato)
    ui.button ("Caso Teste", on_click=lambda: ui.navigate.to('/automato'))


@ui.page('/automato')
def automato_page():


    def avancar():
        try:
            passo = automato.proximoPasso()
            svg = gerarSvgAutomatoDestacado(automato, passo)
            grafo.set_content(svg)

            state['pilha'] = passo.pilha
            state['indice'] = passo.posicaoFita
            renderizar()

        except ValueError as e:
            ui.notify(e)

    def retroceder():
        try:
            passo = automato.passoAnterior()
            svg = gerarSvgAutomatoDestacado(automato, passo)
            grafo.set_content(svg)

            state['pilha'] = passo.pilha
            state['indice'] = passo.posicaoFita
            renderizar()

        except ValueError as e:
            ui.notify(e)

    def inserirPalavra():
        palavra = i_palavra.value
        try:
            feedback = automato.calcularPassos(palavra)
        except ValueError as e:
            ui.notify(e)

        feed.set_text(f"Feedback = {feedback}")

        if feedback == "ACEITA":
            feed.style("color: green; font-weight: bold;")
        elif feedback == "REJEITA":
            feed.style("color: red; font-weight: bold;")

        
        passo = automato.passoAtual()
        svg = gerarSvgAutomatoDestacado(automato, passo)
        grafo.set_content(svg)

        ui.button.enable(a)
        ui.button.enable(r)

        state['pilha'] = passo.pilha
        state['indice'] = passo.posicaoFita
        state['palavra'] = palavra
        renderizar()

    state = {
    'palavra': '',
    'indice': 0,
    'pilha': []
    }

    def renderizar():
        # Limpa e renderiza a fita e pilha
        fita_area.clear()
        pilha_area.clear()

        with fita_area:
            with ui.row().classes('items-center gap-1'):
                for i, c in enumerate(state['palavra']):
                    ui.label(c).classes(
                        'border rounded px-2 py-1 text-xl '
                        + ('bg-yellow-300 font-bold' if i == state['indice'] else '')
                    )

        with pilha_area:
            with ui.column().classes('border rounded p-2 w-16 items-center'):
                ui.label("Topo").classes("text-xs")
                for simbolo in reversed(state['pilha']):
                    ui.label(simbolo).classes('border w-full text-center py-1')






    with ui.row().classes('items-center'):
        i_palavra = ui.input(label="Digite a palavra")
        feed = ui.label (f"Feedback = ")
    ui.button("Inserir palavra", on_click=inserirPalavra)

    with ui.row():
            r = ui.button('Retroceder', on_click=retroceder).classes('mr-2')
            a = ui.button('Avançar', on_click=avancar).classes('ml-2')
            ui.button("Voltar", on_click=lambda: ui.navigate.to('/'))

    ui.button.disable(a)
    ui.button.disable(r)

    grafo = ui.html("", sanitize=False)
    gerar(grafo)
    #ui.space().classes("h-16")

    with ui.row().classes('items-start w-full'):
        # Áreas vazias que serão atualizadas depois
        fita_area = ui.row().classes('flex-grow')
        pilha_area = ui.column().style('width: 160px')


def run():
    ui.run()