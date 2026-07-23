import heapq

class AgenteBuscaHeuristica:
    def __init__(self):
        # Aqui no futuro podemos adicionar configurações de memória da busca
        pass

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
                    return caminho[0]
                return None
            
            assinatura_estado = (pos_atual, tuple(estado_atual.items()))
            if assinatura_estado in visitados:
                continue
            visitados.add(assinatura_estado)

            vizinhos = grafo[pos_atual]

            for acao, proxima_pos in vizinhos.items():
                if posicao_inimigo is not None and proxima_pos == posicao_inimigo:
                    continue

                novo_estado= estado_atual.copy()
                novo_estado[proxima_pos] = 1

                novo_g = g_atual + 1
                novo_h = self._calcular_heuristica(novo_estado, proxima_pos)
                novo_f = novo_g + novo_h

                novo_caminho = caminho + [acao]

                contador += 1
                heapq.heappush(fila, (novo_f, contador, novo_g, proxima_pos, novo_estado, novo_caminho))