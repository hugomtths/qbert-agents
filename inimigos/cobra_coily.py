import random

class CobraCoily:
    def __init__(self, nivel_base=5):
        self.estado = "OVO"
        self.nivel_base = nivel_base

    def _calcular_distancia_isometrica(self, no_atual, no_destino):
        l1, c1 = no_atual
        l2, c2 = no_destino
        
        delta_l = l2 - l1
        delta_c = c2 - c1
        
        return max(abs(delta_l), abs(delta_c), abs(delta_l - delta_c))

    def obter_acao(self, posicao_coily, posicao_qbert, grafo):
        """
        Retorna a ação da Coily dependendo do seu estado atual (OVO ou COBRA).
        """
        if posicao_coily not in grafo:
            return None

        linha_atual, coluna_atual = posicao_coily

        # Algoritmo de movimentação aleatória direcionada
        if self.estado == "OVO":
            if linha_atual >= self.nivel_base:
                self.estado = "COBRA"
                print("O ovo roxo chocou! A Coily virou uma COBRA e começou a caçar!")
            else:
                acoes_possiveis = []
                vizinhos = grafo[posicao_coily]
                
                for acao, proxima_pos in vizinhos.items():
                    if proxima_pos[0] == linha_atual + 1:
                        acoes_possiveis.append(acao)

                if acoes_possiveis:
                    return random.choice(acoes_possiveis)
                return None

        # Algoritmo de Busca Gulosa
        if self.estado == "COBRA":
            if posicao_coily == posicao_qbert:
                return None

            vizinhos = grafo[posicao_coily]
            if not vizinhos:
                return None

            melhor_acao = None
            menor_distancia = float('inf')

            for acao, proxima_pos in vizinhos.items():
                distancia = self._calcular_distancia_isometrica(proxima_pos, posicao_qbert)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_acao = acao

            return melhor_acao