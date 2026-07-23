import random
from inimigos.bola_verde import BolaVerde
from inimigos.cobra_coily import CobraCoily

class QbertEnv:
    def __init__(self, niveis=6, com_inimigos=False):
        self.niveis = niveis
        self.com_inimigos = com_inimigos
        self.grafo = {}
        self.estado_blocos = {}
        self._construir_piramide()

    def _construir_piramide(self):
        for linha in range(self.niveis):
            for coluna in range(linha + 1):
                no = (linha, coluna)
                self.grafo[no] = self._obter_vizinhos(linha, coluna)
                self.estado_blocos[no] = 0

    def _obter_vizinhos(self, l, c):
        vizinhos = {}
        
        if l + 1 < self.niveis:
            vizinhos['baixo_esq'] = (l + 1, c)
            vizinhos['baixo_dir'] = (l + 1, c + 1)
            
        if l - 1 >= 0:
            if c - 1 >= 0:
                vizinhos['cima_esq'] = (l - 1, c - 1)
            if c <= l - 1:
                vizinhos['cima_dir'] = (l - 1, c)
                
        return vizinhos
    
    def reset(self):
        for no in self.estado_blocos:
            self.estado_blocos[no] = 0
            
        self.posicao_agente = (0, 0)
        self.estado_blocos[self.posicao_agente] = 1

        self.bola_verde = BolaVerde()
        self.bola_verde.ativa = False
        self.bola_verde.posicao = None

        self.passos_rodada = 0
        self.coily = CobraCoily()
        if self.com_inimigos:
            self.posicao_coily = (1, 1)
            self.coily.ativa = False
        else:
            self.posicao_coily = None
            self.coily.ativa = False
        
        return self.posicao_agente

    def step(self, acao):
        vizinhos = self.grafo[self.posicao_agente]
        
        if acao in vizinhos:
            self.posicao_agente = vizinhos[acao]
            self.passos_rodada += 1

            # Coily só aparece após 8 passos, se o jogo estiver com inimigos
            if self.com_inimigos and not self.coily.ativa and self.passos_rodada >= 8:
                self.coily.ativa = True
                print("4 segundos se passaram: O ovo da Coily surgiu em (1, 1)!")
            
            # --- COLISÃO 1: Q*bert pulou direto em algum inimigo? ---
            if self.com_inimigos:
                if self.coily.ativa and self.posicao_agente == self.posicao_coily:
                    return self.posicao_agente, -100, False
                if self.bola_verde.ativa and self.posicao_agente == self.bola_verde.posicao:
                    return self.posicao_agente, -100, False

            # --- MOVIMENTAÇÃO E SPAWN DOS INIMIGOS ---
            if self.com_inimigos:
                if self.coily.ativa:
                    acao_coily = self.coily.obter_acao(self.posicao_coily, self.posicao_agente, self.grafo)
                    if acao_coily and acao_coily in self.grafo[self.posicao_coily]:
                        self.posicao_coily = self.grafo[self.posicao_coily][acao_coily]
                
                if not self.bola_verde.ativa:
                    if random.random() < 0:
                        self.bola_verde.ativa = True
                        self.bola_verde.posicao = (1, random.choice([0, 1]))
                else:
                    self.bola_verde.mover(self.niveis)

                # --- COLISÃO 2: Algum inimigo se moveu e alcançou o Q*bert? ---
                if self.coily.ativa and self.posicao_agente == self.posicao_coily:
                    return self.posicao_agente, -100, False
                if self.bola_verde.ativa and self.posicao_agente == self.bola_verde.posicao:
                    return self.posicao_agente, -100, False
            
            recompensa = -1
            if self.estado_blocos[self.posicao_agente] == 0:
                self.estado_blocos[self.posicao_agente] = 1
                recompensa = 10
                
            vitoria = all(estado == 1 for estado in self.estado_blocos.values())
            if vitoria:
                recompensa = 100
                
            return self.posicao_agente, recompensa, vitoria
            
        else:
            return self.posicao_agente, -100, False