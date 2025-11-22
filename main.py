# Simulador Autômato Finito Determístico com Pilha 
# M = (Σ, Q, δ, q0, F, V)
# Σ alfabeto de símbolos de entrada
# Q conjunto finito de estados
# δ função programa ou função de transição
# q0 estado inicial do autômato tal que q0 ∈ Q
# F conjunto de estados finais tal que F ⊆ Q
# V alfabeto auxiliar ou alfabeto da pilha

# Uma palavra é aceita caso a simulação termine em um Estado Final e a fita estiver completamente consuminda, 
# independentemente do estado final da pilha

# ε == movimento vazio (não ler nem gravar)
# ? == significa um teste, indicando se a pilha está vazia ou se a fita estiver vazia (todos os símbolos lidos)

import sys
from interface.web_app import run
from terminal.run_terminal import terminal

if __name__ in {"__main__", "__mp_main__"}:
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        run()
    else:
        terminal()
