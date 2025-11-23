from nicegui import ui
from interface.grafos import gerarSvgAutomato
from interface.grafos import gerarSvgAutomatoDestacado
from automato.automato import Automato
import copy


automato = Automato()
estadosAtuais = set()
estadosFinaisAtuais = set()
alfabetoFitaAtual = set()
alfabetoPilhaAtual = set()

@ui.page('/')
def index():
    ui.add_head_html("""
        <style>
            .input-pequeno .q-field__label {
                font-size: 12px; 
            }
        </style>
    """)

    def avancar(grafo, areaFita, areaPilha):
        try:
            passo = automato.proximoPasso()
            svg = gerarSvgAutomatoDestacado(automato, passo)
            grafo.set_content(svg)

            state['pilha'] = passo.pilha
            state['indice'] = passo.posicaoFita
            renderizarFitaPilha(areaFita, areaPilha)

        except ValueError as e:
            ui.notify(e)

    def retroceder(grafo, areaFita, areaPilha):
        try:
            passo = automato.passoAnterior()
            svg = gerarSvgAutomatoDestacado(automato, passo)
            grafo.set_content(svg)

            state['pilha'] = passo.pilha
            state['indice'] = passo.posicaoFita
            renderizarFitaPilha(areaFita, areaPilha)

        except ValueError as e:
            ui.notify(e)

    def inserirPalavra(i_palavra, grafo, feed, r, a, areaFita, areaPilha):
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
        state['palavra'] = palavra + 'λ'
        renderizarFitaPilha(areaFita, areaPilha)

    state = {
    'palavra': '',
    'indice': 0,
    'pilha': []
    }

        
    def renderizarAutomato():
        areaAutomato.clear()
        with areaAutomato:
            with ui.row().classes('items-center'):
                i_palavra = ui.input(label="Digite a palavra")
                feed = ui.label (f"Feedback = ").classes('text-xl')
            # é necessario usar lambda para usar elemtos da ui como argumentos. A função é executada logo no inicio e seu retorno
            # vai para o onlick do botão. Assim, se os elementos estiverem vazios, ela retorna None e o onclick não faz nada.
            # Se usar lambda, o argumento do onclick será a própria função.
            ui.button("Inserir palavra", on_click=lambda: inserirPalavra(i_palavra, grafo, feed, r, a, areaFita, areaPilha))

            with ui.row():
                    r = ui.button('Retroceder', on_click=lambda: retroceder(grafo, areaFita, areaPilha)).classes('mr-2')
                    a = ui.button('Avançar', on_click=lambda: avancar(grafo, areaFita, areaPilha)).classes('ml-2')

            ui.button.disable(a)
            ui.button.disable(r)

            svg = gerarSvgAutomato(automato)
            grafo = ui.html(svg, sanitize=False)

            with ui.row().classes('items-start w-full'):
                areaFita = ui.row().classes('flex-grow')
                areaPilha = ui.column().style('width: 160px')
    
    def renderizarFitaPilha(areaFita, areaPilha):
        areaFita.clear()
        areaPilha.clear()

        with areaFita:
            with ui.row().classes('items-center gap-1'):
                for i, c in enumerate(state['palavra']):
                    ui.label(c).classes(
                        'border rounded px-2 py-1 text-xl '
                        + ('bg-yellow-300 font-bold' if i == state['indice'] else '')
                    )

        with areaPilha:
            with ui.column().classes('border rounded p-2 w-16 items-center'):
                ui.label("Topo").classes("text-xs")
                for simbolo in reversed(state['pilha']):
                    ui.label(simbolo).classes('border w-full text-center py-1')

    def atualizarTransicao():
        t.clear()
        with t:
            for i, (chave, valor) in enumerate(automato.transicoes.items()):
                ui.label(f"δ({i}): ({chave[0]}, {chave[1]}, {chave[2]}, {valor[0]}, {valor[1]} )").style("font-size: 18px")
    
    def adicionarTransicao():
        try:
            origem = i_origem.value
            fita = i_fita.value
            pilha = i_pilha.value
            destino = i_destino.value
            empilha = i_empilha.value
            automato.inserirTransicao(origem, fita, pilha, destino, empilha)
            atualizarTransicao()
        except ValueError as e:
            ui.notify(e)
    
    def removerTransicao():
        try:
            origem = i_origem.value
            fita = i_fita.value
            pilha = i_pilha.value
            automato.removerTransicao(origem, fita, pilha)
            atualizarTransicao()
        except ValueError as e:
            ui.notify(e)

    def gerarAutomato():
        global automato
        global estadosAtuais 
        global estadosFinaisAtuais
        global alfabetoFitaAtual
        global alfabetoPilhaAtual 

        # em caso de erro, dar rollback
        backup = copy.deepcopy(automato)
        try:

            if i_estadoInicial.error:
                raise ValueError("Apenas 1 estado inicial é permitido")
        
            estadoInicial = i_estadoInicial.value

            estados = {e.strip() for e in i_estados.value.split(',')}
            automato.inserirEstados(*estados)

            temp = estadosAtuais - estados
            automato.removerEstados(*temp)

            automato.inserirEstadoInicial(estadoInicial)

            estadosFinais = {e.strip() for e in i_estadosFinais.value.split(',')}
            automato.inserirEstadosFinais(*estadosFinais)

            temp = estadosFinaisAtuais - estadosFinais
            automato.removerEstadosFinais(*temp)

            alfabetoFita = {s.strip() for s in i_alfabetoFita.value.split(',')}
            automato.inserirAlfabeto(*alfabetoFita)


            temp = alfabetoFitaAtual - alfabetoFita
            automato.removerAlfabeto(*temp)

            alfabetoPilha = {s.strip() for s in i_alfabetoPilha.value.split(',')}
            automato.inserirAlfabetoPilha(*alfabetoPilha)

            temp = alfabetoPilhaAtual - alfabetoPilha
            automato.removerAlfabetoPilha(*temp) 

            estadosAtuais = estados
            estadosFinaisAtuais = estadosFinais
            alfabetoFitaAtual = alfabetoFita
            alfabetoPilhaAtual = alfabetoPilha
            #renderizarAutomato()
            ui.button.enable(g)
            atualizarTransicao()

        except ValueError as e:
            ui.notify(e)
            automato = backup

    with ui.row().classes("w-full"):
        with ui.column():
            with ui.row().classes('items-end'):
                with ui.column().classes("border p-4 rounded"):
                    ui.label("Estados: ")
                    i_estados = ui.input("Separados por vírgula").classes('w-64')

                    ui.label("Estado inicial:")
                    i_estadoInicial = ui.input('Apenas 1', validation={
                    'Apenas 1 estado inicial': lambda v: ',' not in v,
                    'Máximo 10 caracteres': lambda v: len(v) <= 10,
                    }).classes('w-64')

                    ui.label("Estados finais:")
                    i_estadosFinais = ui.input("Separados por vírgula").classes('w-64')

                    ui.label("Alfabeto Fita: ")
                    i_alfabetoFita = ui.input("Separados por vírgula").classes('w-64')

                    ui.label("Alfabeto Pilha: ")
                    i_alfabetoPilha = ui.input("Separados por vírgula").classes('w-64')
                with ui.column():
                    ui.label("ε = Não ler/gravar na fita/pilha")
                    ui.label("? = Verificar vazio")
                    ui.button("Definir Autômato", on_click=gerarAutomato)
                    g = ui.button("Gerar Autômato", on_click=renderizarAutomato)
                    ui.button.disable(g)

            with ui.column().classes("border p-4 rounded"):

                ui.label("Adicionar Transição (δ):")
                with ui.row():
                    i_origem = ui.input(label="Origem").classes('w-15 input-pequeno')
                    i_fita = ui.input(label="Símbolo Fita").classes('w-15 input-pequeno')
                    i_pilha = ui.input(label="Topo Pilha").classes('w-15 input-pequeno')
                    i_destino = ui.input(label="Destino").classes('w-15 input-pequeno')
                    i_empilha = ui.input(label="Empilha").classes('w-15 input-pequeno')
                    with ui.column().classes('items-center mt-[-18px]'):
                        ui.button("Adicionar", on_click=adicionarTransicao)
                        ui.button("Remover", on_click=removerTransicao)

                ui.label("Transições Atuais:")
                t = ui.label('')

        areaAutomato = ui.column()


def run():
    ui.run()