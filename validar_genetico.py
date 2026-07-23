from ambiente.qbert_env import QbertEnv
from agentes.agente_genetico import AgenteGenetico

def rodar_teste_robustez(num_testes=30):
    print(f"🚀 Iniciando teste de validação com {num_testes} rodadas...\n")
    
    env = QbertEnv(niveis=6)
    vitorias = 0
    vitorias_otimas = 0  # Contador para vitórias perfeitas (<= 23 passos)
    passos_vitoriosos = []
    
    for i in range(1, num_testes + 1):
        # Desativa saídas longas se houver no seu agente, focando só no resultado
        agente_gen = AgenteGenetico(tamanho_populacao=150, taxa_mutacao=0.05, tamanho_cromossomo=40)
        melhor = agente_gen.treinar(env, num_geracoes=1000)
        
        # Faz uma simulação limpa do melhor indivíduo para verificar o resultado
        env.reset()
        passos = 0
        venceu = False
        
        for acao in melhor.cromossomo:
            passos += 1
            _, recompensa, vitoria = env.step(acao)
            if vitoria:
                venceu = True
                break
            elif recompensa in (-10, -100):
                break
                
        if venceu:
            vitorias += 1
            passos_vitoriosos.append(passos)
            
            # Verifica se atingiu a perfeição matemática da rota
            if passos <= 23:
                vitorias_otimas += 1
                print(f"Rodada {i:02d}: 🏆 VITÓRIA PERFEITA em {passos} passos!")
            else:
                print(f"Rodada {i:02d}: ✅ VITÓRIA em {passos} passos!")
        else:
            print(f"Rodada {i:02d}: ❌ FALHA")

    # --- RESUMO FINAL ---
    taxa_sucesso = (vitorias / num_testes) * 100
    taxa_otimas = (vitorias_otimas / num_testes) * 100
    media_passos = sum(passos_vitoriosos) / len(passos_vitoriosos) if passos_vitoriosos else 0
    
    print("\n" + "="*45)
    print("📊 RESULTADO DA VALIDAÇÃO")
    print("="*45)
    print(f"Taxa de Sucesso Geral:  {taxa_sucesso:.1f}% ({vitorias}/{num_testes})")
    print(f"Média de Passos:        {media_passos:.1f}")
    print(f"Ótimos Globais (≤ 23):  {taxa_otimas:.1f}% ({vitorias_otimas}/{num_testes})")
    print("="*45)

if __name__ == "__main__":
    rodar_teste_robustez(30)