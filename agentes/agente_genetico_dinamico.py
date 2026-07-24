import random

class Individuo:
    def __init__(self, tamanho_cromossomo=65):
        self.tamanho_cromossomo = tamanho_cromossomo
        self.acoes_possiveis = ['baixo_esq', 'baixo_dir', 'cima_esq', 'cima_dir']
        self.cromossomo = [random.choice(self.acoes_possiveis) for _ in range(tamanho_cromossomo)]
        self.fitness = 0

    def calcular_fitness(self, env, num_simulacoes=3):
        """
        Testa o cromossomo múltiplas vezes no ambiente para garantir consistência contra os inimigos e aplica punição progressiva para mortes precoces.
        """
        fitness_total = 0

        for _ in range(num_simulacoes):
            env.reset()
            blocos_pintados = 0
            passos_seguros = 0
            pulos_repetidos = 0
            pos_anterior = None
            movimentos_em_loop = 0
            morreu = False
            venceu = False

            for acao in self.cromossomo:
                pos_atual = env.posicao_agente
                vizinhos_validos = env.grafo.get(pos_atual, {})

                if acao not in vizinhos_validos:
                    idx_borda = abs(hash(acao)) % len(vizinhos_validos)
                    acao_executada = list(vizinhos_validos.keys())[idx_borda]
                else:
                    acao_executada = acao

                posicao_inimigo = getattr(env, 'posicao_coily', None)
                if posicao_inimigo and getattr(env.coily, 'ativa', False):
                    if posicao_inimigo in vizinhos_validos.values():
                        saidas_seguras = [act for act, pos in vizinhos_validos.items() if pos != posicao_inimigo]
                        if saidas_seguras:
                            idx_fuga = abs(hash(acao_executada)) % len(saidas_seguras)
                            acao_executada = saidas_seguras[idx_fuga]

                # Executa a ação segura no ambiente
                proxima_pos = vizinhos_validos.get(acao_executada)

                if proxima_pos and env.estado_blocos.get(proxima_pos) == 1:
                    pulos_repetidos += 1

                _, recompensa, vitoria = env.step(acao_executada)

                if proxima_pos == pos_anterior:
                    movimentos_em_loop += 1
                pos_anterior = pos_atual

                if recompensa == -100 or recompensa == -10:
                    morreu = True
                    break

                passos_seguros += 1

                if recompensa > 0:
                    blocos_pintados += 1

                if vitoria:
                    venceu = True
                    break

            nota_simulacao = (blocos_pintados * 4000) - (passos_seguros * 10) - (pulos_repetidos * 200) - (movimentos_em_loop * 8000)
            
            if morreu:
                passos_faltantes = self.tamanho_cromossomo - passos_seguros
                nota_simulacao -= (10000 + (passos_faltantes * 400))
            
            if venceu:
                passos_economizados = self.tamanho_cromossomo - passos_seguros
                nota_simulacao += 150000 + (passos_economizados * 5000)

            fitness_total += nota_simulacao

        # A nota final é a média do desempenho nas 3 simulações
        self.fitness = fitness_total / num_simulacoes
        return self.fitness

class AgenteGeneticoDinamico:
    def __init__(self, tamanho_populacao=100, taxa_mutacao=0.05, tamanho_cromossomo=65):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.tamanho_cromossomo = tamanho_cromossomo
        self.acoes_possiveis = ['baixo_esq', 'baixo_dir', 'cima_esq', 'cima_dir']

        self.populacao = [Individuo(tamanho_cromossomo) for _ in range(tamanho_populacao)]

    def _selecao_torneio(self, k=3):
        """
        Pega 'k' indivíduos aleatórios da população e escolhe o melhor entre eles.
        """
        competidores = random.sample(self.populacao, k)
        return max(competidores, key=lambda ind: ind.fitness)

    def _cruzamento(self, pai1, pai2):
        """
        Cruzamento de Dois Pontos: Preserva melhor os blocos de passos que já funcionam.
        """
        p1 = random.randint(1, self.tamanho_cromossomo - 2)
        p2 = random.randint(p1 + 1, self.tamanho_cromossomo - 1)
        
        filho = Individuo(self.tamanho_cromossomo)

        filho.cromossomo = (pai1.cromossomo[:p1] + 
                            pai2.cromossomo[p1:p2] + 
                            pai1.cromossomo[p2:])
        
        return filho

    def _mutacao(self, individuo):
        """
        Percorre cada pulo e, com uma chance bem baixa, troca por outro aleatório.
        """
        for i in range(self.tamanho_cromossomo):
            if random.random() < self.taxa_mutacao:
                individuo.cromossomo[i] = random.choice(self.acoes_possiveis)
        return individuo

    def treinar(self, env, num_geracoes=150):
        """
        Executa o ciclo de evolução do Algoritmo Genético ao longo das gerações.
        """
        melhor_individuo_geral = None

        for geracao in range(1, num_geracoes + 1):
            for individuo in self.populacao:
                individuo.calcular_fitness(env)

            self.populacao.sort(key=lambda ind: ind.fitness, reverse=True)
            campeao_da_geracao = self.populacao[0]

            if melhor_individuo_geral is None or campeao_da_geracao.fitness > melhor_individuo_geral.fitness:
                melhor_individuo_geral = Individuo(self.tamanho_cromossomo)
                melhor_individuo_geral.cromossomo = list(campeao_da_geracao.cromossomo)
                melhor_individuo_geral.fitness = campeao_da_geracao.fitness

            print(f"Geração {geracao:03d} | Melhor Fitness da Rodada: {campeao_da_geracao.fitness:.0f} | Recorde Geral: {melhor_individuo_geral.fitness:.0f}")

            if melhor_individuo_geral.fitness >= 100000 and not hasattr(self, '_ja_avisou_vitoria'):
                print("\nPRIMEIRA VITÓRIA ALCANÇADA! Continuando o treino para otimizar os passos...")
                self._ja_avisou_vitoria = True

            nova_populacao = []

            for i in range(min(10, len(self.populacao))):
                clone = Individuo(self.tamanho_cromossomo)
                clone.cromossomo = list(self.populacao[i].cromossomo)
                clone.fitness = self.populacao[i].fitness
                nova_populacao.append(clone)

            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self._selecao_torneio()
                pai2 = self._selecao_torneio()
                filho = self._cruzamento(pai1, pai2)
                filho = self._mutacao(filho)
                nova_populacao.append(filho)

            self.populacao = nova_populacao

        print("\n=== TREINAMENTO CONCLUÍDO ===")
        print(f"Pontuação máxima alcançada: {melhor_individuo_geral.fitness}")

        return melhor_individuo_geral
