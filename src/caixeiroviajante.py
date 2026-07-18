import itertools

class PlanejamentoEntregasTSP:
    def __init__(self, logistica):
        self.logistica = logistica

    def distancia_entre(self, origem, destino):
        """Usa o Dijkstra do módulo 7 para achar a distância real."""
        # Se for o mesmo ponto, a distância é 0
        if origem == destino:
            return 0
        
        _, dist = self.logistica.calcular_rota_mais_rapida(origem, destino)
        return dist

    def calcular_rota_tsp_exata(self, origem_matriz, bairros_entrega):
        """
        Resolve o Problema do Caixeiro Viajante (TSP).
        Garante a menor rota visitando todos os bairros e voltando à matriz.
        """
        menor_distancia = float('inf')
        melhor_rota = []
        
        # itertools.permutations testa todas as ordens possíveis de visitação (O(N!))
        for permutacao in itertools.permutations(bairros_entrega):
            distancia_atual = 0
            ponto_atual = origem_matriz
            rota_valida = True
            
            # Vai da matriz -> bairro 1 -> bairro 2 ...
            for destino in permutacao:
                dist = self.distancia_entre(ponto_atual, destino)
                if dist == float('inf'):
                    rota_valida = False
                    break
                distancia_atual += dist
                ponto_atual = destino
            
            if not rota_valida:
                continue

            # Volta do último bairro visitado para a origem
            dist_volta = self.distancia_entre(ponto_atual, origem_matriz)
            if dist_volta == float('inf'):
                continue
                
            distancia_atual += dist_volta
            
            if distancia_atual < menor_distancia:
                menor_distancia = distancia_atual
                # Monta a string final da rota
                melhor_rota = [origem_matriz] + list(permutacao) + [origem_matriz]
                
        return melhor_rota, menor_distancia