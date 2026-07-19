import heapq
from collections import defaultdict, deque

class PesadeloLogistico:
    def __init__(self):
        # dijkstra e kruskal
        self.grafo_distancias = defaultdict(list)
        # fluxo bfs edmonds
        self.grafo_capacidades = defaultdict(dict)
        self.arestas = [] 
        self.vertices = set()

    def adicionar_rota(self, origem, destino, tempo_distancia, capacidade_pedidos):

        self.vertices.add(origem)
        self.vertices.add(destino)
        
        # dijkstra
        self.grafo_distancias[origem].append((destino, tempo_distancia))
        self.grafo_distancias[destino].append((origem, tempo_distancia))
        
        # kruskal
        self.arestas.append((tempo_distancia, origem, destino))
        
        self.grafo_capacidades[origem][destino] = capacidade_pedidos
        if origem not in self.grafo_capacidades[destino]:
            self.grafo_capacidades[destino][origem] = 0

    def calcular_menor_infraestrutura(self):
        parent = {v: v for v in self.vertices}
        rank = {v: 0 for v in self.vertices}

        def find(v):
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(u, v):
            root1 = find(u)
            root2 = find(v)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root2] += 1
                return True
            return False

        self.arestas.sort()
        rede_minima = []
        custo_total = 0

        for custo, u, v in self.arestas:
            if union(u, v):
                rede_minima.append((u, v, custo))
                custo_total += custo

        return rede_minima, custo_total

    def calcular_rota_mais_rapida(self, origem, destino):
        if origem not in self.vertices or destino not in self.vertices:
            return None, float('inf')

        distancias = {v: float('inf') for v in self.vertices}
        distancias[origem] = 0
        pq = [(0, origem)]
        caminho = {origem: None}

        while pq:
            dist_atual, u = heapq.heappop(pq)

            if dist_atual > distancias[u]:
                continue

            if u == destino:
                break

            for vizinho, peso in self.grafo_distancias[u]:
                distancia_nova = dist_atual + peso
                if distancia_nova < distancias[vizinho]:
                    distancias[vizinho] = distancia_nova
                    caminho[vizinho] = u
                    heapq.heappush(pq, (distancia_nova, vizinho))
        rota = []
        atual = destino
        while atual is not None:
            rota.append(atual)
            atual = caminho.get(atual)
        rota.reverse()

        return rota, distancias[destino]

    def calcular_capacidade_maxima(self, origem, destino):
        
        def bfs_caminho_aumento(grafo_residual, s, t, parent):
            visitado = {v: False for v in self.vertices}
            fila = deque([s])
            visitado[s] = True

            while fila:
                u = fila.popleft()
                for vizinho, capacidade in grafo_residual[u].items():
                    if not visitado[vizinho] and capacidade > 0:
                        fila.append(vizinho)
                        visitado[vizinho] = True
                        parent[vizinho] = u
                        if vizinho == t:
                            return True
            return False

        grafo_residual = {u: {v: cap for v, cap in vizinhos.items()} 
                          for u, vizinhos in self.grafo_capacidades.items()}
        
        parent = {v: None for v in self.vertices}
        fluxo_maximo = 0

        while bfs_caminho_aumento(grafo_residual, origem, destino, parent):
            fluxo_caminho = float('inf')
            s = destino
            while s != origem:
                fluxo_caminho = min(fluxo_caminho, grafo_residual[parent[s]][s])
                s = parent[s]

            fluxo_maximo += fluxo_caminho
            v = destino
            while v != origem:
                u = parent[v]
                grafo_residual[u][v] -= fluxo_caminho
                if u not in grafo_residual[v]:
                    grafo_residual[v][u] = 0
                grafo_residual[v][u] += fluxo_caminho
                v = parent[v]

        return fluxo_maximo