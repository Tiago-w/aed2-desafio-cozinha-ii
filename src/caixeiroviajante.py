import itertools

class PlanejamentoEntregasTSP:
    def __init__(self, logistica):
        self.logistica = logistica

    def distancia_entre(self, origem, destino):
        if origem == destino:
            return 0
        
        _, dist = self.logistica.calcular_rota_mais_rapida(origem, destino)
        return dist

    def calcular_rota_tsp_exata(self, origem_matriz, bairros_entrega):
        
        menor_distancia = float('inf')
        melhor_rota = []
        
        for permutacao in itertools.permutations(bairros_entrega):
            distancia_atual = 0
            ponto_atual = origem_matriz
            rota_valida = True
            
            #visita todos os bairros
            for destino in permutacao:
                dist = self.distancia_entre(ponto_atual, destino)
                if dist == float('inf'):
                    rota_valida = False
                    break
                distancia_atual += dist
                ponto_atual = destino
            
            if not rota_valida:
                continue

            # volta origem
            dist_volta = self.distancia_entre(ponto_atual, origem_matriz)
            if dist_volta == float('inf'):
                continue
                
            distancia_atual += dist_volta
            
            if distancia_atual < menor_distancia:
                menor_distancia = distancia_atual
                melhor_rota = [origem_matriz] + list(permutacao) + [origem_matriz]
                
        return melhor_rota, menor_distancia