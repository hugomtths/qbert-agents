from ambiente.qbert_env import QbertEnv
from agentes.busca_heuristica import AgenteBuscaHeuristica
import interface # Importando a nossa tela do Pygame

def principal():
    print("=== BEM-VINDO AO Q*BERT AI ===")
    print("1. Busca Heurística (A*)")
    print("2. Q-Learning (Em breve)")
    print("3. Aleatório/Outro (Em breve)")
    
    escolha = input("\nEscolha qual agente vai jogar (1/2/3): ")
    
    env = QbertEnv(niveis=6)
    env.reset() # Inicializa o ambiente
    
    # Seleção de Agentes
    if escolha == '1':
        agente = AgenteBuscaHeuristica()
        print("\nIniciando Busca Heurística...")
    else:
        print("\nOpção inválida ou não implementada. Usando Busca Heurística por padrão.")
        agente = AgenteBuscaHeuristica()
        
    # Passamos o controle para a interface gráfica
    interface.rodar(env, agente)

if __name__ == "__main__":
    principal()