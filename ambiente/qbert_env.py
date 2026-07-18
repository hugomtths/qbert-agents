class QbertEnv:
    def __init__(self, niveis=6):
        self.niveis = niveis
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
        
        return self.posicao_agente

    def step(self, acao):
        vizinhos = self.grafo[self.posicao_agente]
        
        if acao in vizinhos:
            self.posicao_agente = vizinhos[acao]
            
            recompensa = 0
            if self.estado_blocos[self.posicao_agente] == 0:
                self.estado_blocos[self.posicao_agente] = 1
                recompensa = 1 
                
            vitoria = all(estado == 1 for estado in self.estado_blocos.values())
            if vitoria:
                recompensa = 10
                
            return self.posicao_agente, recompensa, vitoria
            
        else:
            return self.posicao_agente, -10, True