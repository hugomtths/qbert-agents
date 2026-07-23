import random
import pickle
from collections import defaultdict

class AgenteReforco:

    def __init__(
        self,
        alpha=0.2,            # Taxa de aprendizado (↑ aprende mais rápido, ↓ aprende mais lentamente)
        gamma=0.95,           # Importância das recompensas futuras (↑ mais visão de longo prazo, ↓ prioriza recompensas imediatas)
        epsilon=1.0,          # Probabilidade inicial de explorar ações aleatórias (↑ mais exploração no início)
        epsilon_min=0.01,     # Valor mínimo de exploração (↑ continua explorando mais, ↓ torna-se mais "ganancioso")
        epsilon_decay=0.9995, # Velocidade de redução do epsilon (↑ reduz mais lentamente, ↓ reduz mais rapidamente)
    ):

        self.alpha = alpha
        self.gamma = gamma

        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.q_table = defaultdict(float)

    def estado_para_chave(self, estado_blocos, posicao):

        return (
            posicao,
            tuple(sorted(estado_blocos.items()))
        )

    def escolher_acao(self, estado_blocos, posicao, grafo):

        estado = self.estado_para_chave(
            estado_blocos,
            posicao
        )

        acoes = list(grafo[posicao].keys())

        # Exploração
        if random.random() < self.epsilon:
            return random.choice(acoes)

        # Exploração da política
        melhor_acao = None
        melhor_valor = float("-inf")

        for acao in acoes:

            valor = self.q_table[(estado, acao)]

            if valor > melhor_valor:
                melhor_valor = valor
                melhor_acao = acao

        if melhor_acao is None:
            return random.choice(acoes)

        return melhor_acao

    def atualizar(
        self,
        estado,
        acao,
        recompensa,
        proximo_estado,
        proximas_acoes,
        terminou
    ):

        atual = self.q_table[(estado, acao)]

        if terminou:
            alvo = recompensa

        else:
            maior_q = max(
                self.q_table[(proximo_estado, a)]
                for a in proximas_acoes
            )

            alvo = recompensa + self.gamma * maior_q

        self.q_table[(estado, acao)] = (
            atual
            + self.alpha * (alvo - atual)
        )

    def treinar(self, env, episodios=5000):
        for episodio in range(episodios):
            posicao = env.reset()
            terminou = False

            while not terminou:
                estado = self.estado_para_chave(
                    env.estado_blocos,
                    env.posicao_agente
                )

                acao = self.escolher_acao(
                    env.estado_blocos,
                    env.posicao_agente,
                    env.grafo
                )

                nova_posicao, recompensa, terminou = env.step(acao)

                proximo_estado = self.estado_para_chave(
                    env.estado_blocos,
                    nova_posicao
                )

                proximas_acoes = list(
                    env.grafo[nova_posicao].keys()
                )

                self.atualizar(
                    estado,
                    acao,
                    recompensa,
                    proximo_estado,
                    proximas_acoes,
                    terminou
                )

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            if episodio % 500 == 0:
                print(
                    f"Episódio {episodio}"
                    f" | epsilon = {self.epsilon:.3f}"
                )

    def obter_acao(self, estado_blocos, posicao, grafo):
        estado = self.estado_para_chave(
            estado_blocos,
            posicao
        )

        acoes = list(grafo[posicao].keys())

        melhor = None
        melhor_q = float("-inf")

        for acao in acoes:
            q = self.q_table[(estado, acao)]

            if q > melhor_q:
                melhor_q = q
                melhor = acao

        if melhor is None:
            return random.choice(acoes)

        return melhor

    def salvar(self, arquivo):
        with open(arquivo, "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def carregar(self, arquivo):
        with open(arquivo, "rb") as f:
            tabela = pickle.load(f)

        self.q_table = defaultdict(float, tabela)