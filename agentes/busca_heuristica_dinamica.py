import heapq

class AgenteBuscaHeuristicaDinamica:
    def __init__(self):
        self.historico_posicoes = []

    def _calcular_distancia_isometrica(self, no_atual, no_destino):
        l1, c1 = no_atual
        l2, c2 = no_destino
        
        delta_l = l2 - l1
        delta_c = c2 - c1
        
        # Fórmula da distância em malha axial (hexagonal/isométrica)
        distancia = max(abs(delta_l), abs(delta_c), abs(delta_l - delta_c))
        
        return distancia
    
    def _calcular_heuristica(self, estado_atual, posicao_agente):
        blocos_vazios = []

        for no, pintado in estado_atual.items():
            if pintado == 0:
                blocos_vazios.append(no)

        if not blocos_vazios:
            return 0
        
        distancias = []
        for bloco in blocos_vazios:
            dist = self._calcular_distancia_isometrica(posicao_agente, bloco)
            distancias.append(dist)

        return min(distancias)

    def _obter_zona_de_perigo(self, posicao_inimigo, grafo):
        if not posicao_inimigo or posicao_inimigo not in grafo:
            return set()
            
        zona_perigo = {posicao_inimigo}
        
        # Adiciona todos os blocos vizinhos à cobra como área de risco
        for vizinho in grafo[posicao_inimigo].values():
            zona_perigo.add(vizinho)
            
        return zona_perigo
    
    def obter_acao(self, estado_atual, posicao_agente, grafo, posicao_inimigo=None):
        fila = []
        contador = 0

        # Mapeia a zona de risco antes de começar a busca
        zona_perigo = self._obter_zona_de_perigo(posicao_inimigo, grafo)

        estado_inicial = estado_atual.copy()
        caminho_inicial = []

        g_inicial = 0
        h_inicial = self._calcular_heuristica(estado_inicial, posicao_agente)
        f_inicial = g_inicial + h_inicial

        heapq.heappush(fila, (f_inicial, contador, g_inicial, posicao_agente, estado_inicial, caminho_inicial))

        visitados = set()

        while fila:
            f_atual, _, g_atual, pos_atual, estado_atual, caminho = heapq.heappop(fila)

            if all(valor == 1 for valor in estado_atual.values()):
                if caminho:
                    acao_escolhida = caminho[0]
                    self.historico_posicoes.append(grafo[posicao_agente][acao_escolhida])
                    if len(self.historico_posicoes) > 8:
                        self.historico_posicoes.pop(0)

                    return acao_escolhida
                
                return None
            
            assinatura_estado = (pos_atual, tuple(estado_atual.items()))
            if assinatura_estado in visitados:
                continue
            visitados.add(assinatura_estado)

            vizinhos = grafo[pos_atual]

            for acao, proxima_pos in vizinhos.items():
                # Se o bloco for perigoso, nós ignoramos e não traçamos caminho por lá
                if proxima_pos in zona_perigo:
                    continue

                novo_estado = estado_atual.copy()
                novo_estado[proxima_pos] = 1

                novo_g = g_atual + 1
                novo_h = self._calcular_heuristica(novo_estado, proxima_pos)

                penalidade_cobra = 0
                if posicao_inimigo:
                    dist_cobra = self._calcular_distancia_isometrica(proxima_pos, posicao_inimigo)
                    if dist_cobra <= 1:
                        penalidade_cobra = 50

                penalidade_pintado = 0
                if estado_atual[proxima_pos] == 1:
                    penalidade_pintado = 35

                penalidade_historico = 0
                if proxima_pos in self.historico_posicoes:
                    continue

                novo_f = novo_g + novo_h + penalidade_cobra + penalidade_pintado

                novo_caminho = caminho + [acao]

                contador += 1
                heapq.heappush(fila, (novo_f, contador, novo_g, proxima_pos, novo_estado, novo_caminho))

       # Se a busca falhou porque tudo em volta é perigoso, tenta fugir
        vizinhos_validos = grafo[posicao_agente]
        if vizinhos_validos and posicao_inimigo:
            melhor_fuga = None
            melhor_pontuacao = -9999
            
            for acao, proxima_pos in vizinhos_validos.items():
                dist_cobra = self._calcular_distancia_isometrica(proxima_pos, posicao_inimigo)
                
                # A pontuação base é ficar o mais longe possível da cobra
                pontuacao = dist_cobra * 10

                # Se o bloco da fuga não está pintado, ganha um bônus gigante
                if estado_atual[proxima_pos] == 0:
                    pontuacao += 50

                # Se já pisou nesse bloco nos últimos turnos, perde muitos pontos!
                if proxima_pos in self.historico_posicoes:
                    pontuacao -= 100
                
                # Se o bloco é suicídio imediato (zona de perigo), perde mil pontos
                if proxima_pos in zona_perigo:
                    pontuacao -= 1000
                
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_fuga = acao
            
            if melhor_fuga:
                self.historico_posicoes.append(vizinhos_validos[melhor_fuga])
                if len(self.historico_posicoes) > 8:
                    self.historico_posicoes.pop(0)
                return melhor_fuga

        if vizinhos_validos:
            acao_aleatoria = list(vizinhos_validos.keys())[0]
            return acao_aleatoria

        return None