from ambiente.qbert_env import QbertEnv
from agentes.busca_heuristica import AgenteBuscaHeuristica
import time

def principal():
    env = QbertEnv(niveis=6)
    agente = AgenteBuscaHeuristica()

    posicao_atual = env.reset()
    jogo_rodando = True
    passos = 0

    print(f"=== INICIANDO Q*BERT (Busca Heurística) ===")
    print(f"Posição inicial: {posicao_atual}")

    while jogo_rodando:
        time.sleep(0.5)

        acao = agente.obter_acao(env.estado_blocos, posicao_atual, env.grafo)

        if acao is None:
            print("\nNenhum caminho encontrado ou objetivo já atingido.")
            break
        
        posicao_atual, recompensa, vitoria = env.step(acao)
        passos += 1

        print(f"Passo {passos} | Ação: {acao} | Posição: {posicao_atual} | Recompensa: {recompensa}")

        if vitoria:
            print(f"\nVITÓRIA! Pirâmide totalmente pintada em {passos} passos.")
            jogo_rodando = False
        elif recompensa == -10:
            print(f"\nGAME OVER! O agente pulou para fora do mapa.")
            jogo_rodando = False

if __name__ == "__main__":
    principal()