import random

class Individuo:
    def __init__(self, tamanho_cromossomo=30):
        self.tamanho_cromossomo = tamanho_cromossomo
        self.acoes_possiveis = ['baixo_esq', 'baixo_dir', 'cima_esq', 'cima_dir']
        self.cromossomo = [random.choice(self.acoes_possiveis) for _ in range(tamanho_cromossomo)]
        self.fitness = 0

    def calcular_fitness(self, env):
        """
        Simula o cromossomo no ambiente sem desenhar na tela, apenas para medir o quão longe essa sequência chega.
        """
        env.reset()
        blocos_pintados = 0
        passos_seguros = 0
        pulos_repetidos = 0
        morreu = False
        venceu = False

        for acao in self.cromossomo:
            pos_atual = env.posicao_agente
            proxima_pos = env.grafo.get(pos_atual, {}).get(acao)

            if proxima_pos and env.estado_blocos.get(proxima_pos) == 1:
                pulos_repetidos += 1

            _, recompensa, vitoria = env.step(acao)

            if recompensa == -100 or recompensa == -10:
                morreu = True
                break

            passos_seguros += 1

            if recompensa > 0:
                blocos_pintados += 1

            if vitoria:
                venceu = True
                break

        self.fitness = (blocos_pintados * 1000) - (passos_seguros * 10) - (pulos_repetidos * 200)
        if morreu:
            self.fitness -= 20000
        if vitoria:
            passos_economizados = self.tamanho_cromossomo - passos_seguros
            self.fitness += 100000 + (passos_economizados * 3000)
        return self.fitness

class AgenteGenetico:
    def __init__(self, tamanho_populacao=50, taxa_mutacao=0.05, tamanho_cromossomo=30):
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

            print(f"Geração {geracao:03d} | Melhor Fitness da Rodada: {campeao_da_geracao.fitness:06d} | Recorde Geral: {melhor_individuo_geral.fitness:06d}")

            if melhor_individuo_geral.fitness >= 100000 and not hasattr(self, '_ja_avisou_vitoria'):
                print("\nPRIMEIRA VITÓRIA ALCANÇADA! Continuando o treino para otimizar os passos...")
                self._ja_avisou_vitoria = True

            nova_populacao = []

            for i in range(min(5, len(self.populacao))):
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
