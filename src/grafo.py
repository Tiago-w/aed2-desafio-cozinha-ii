from collections import defaultdict, deque
import heapq


class GrafoDependencias:

    def identificar_comunidades(self):
        """Módulo 8: Identifica famílias de receitas interligadas (Componentes Conexos via DFS)"""
        visitados = set()
        comunidades = []

        adj_nao_direcionada = defaultdict(list)
        for u in self.vertices:
            for v in self.adjacencias[u]:
                adj_nao_direcionada[u].append(v)
                adj_nao_direcionada[v].append(u)

        for vertice in self.vertices:
            if vertice not in visitados:
                comunidade_atual = []
                fila = deque([vertice])
                while fila:
                    atual = fila.popleft()
                    if atual not in visitados:
                        visitados.add(atual)
                        comunidade_atual.append(atual)
                        for vizinho in adj_nao_direcionada[atual]:
                            if vizinho not in visitados:
                                fila.append(vizinho)
                comunidades.append(comunidade_atual)

        return [c for c in comunidades if len(c) > 1]

    def __init__(self):
        self.adjacencias = defaultdict(list)
        self.grau_entrada = defaultdict(int)
        self.vertices = set()

    def adicionar_receita(self, receita_id):
        self.vertices.add(receita_id)
        if receita_id not in self.grau_entrada:
            self.grau_entrada[receita_id] = 0

    def adicionar_dependencia(self, prerequisito, receita_alvo):
        """Define que 'prerequisito' precisa ser concluído antes de 'receita_alvo'."""
        self.adicionar_receita(prerequisito)
        self.adicionar_receita(receita_alvo)

        self.adjacencias[prerequisito].append(receita_alvo)
        self.grau_entrada[receita_alvo] += 1

    def gerar_ordem_producao(self):
        """Executa a Ordenação Topológica (Algoritmo de Kahn)."""
        fila = deque([v for v in self.vertices if self.grau_entrada[v] == 0])
        ordem_execucao = []
        processados = 0

        while fila:
            atual = fila.popleft()
            ordem_execucao.append(atual)
            processados += 1

            for vizinho in self.adjacencias[atual]:
                self.grau_entrada[vizinho] -= 1
                if self.grau_entrada[vizinho] == 0:
                    fila.append(vizinho)

        if processados != len(self.vertices):
            return None, "Erro: Inconsistência detectada (Ciclo de dependências)!"

        return ordem_execucao, "Sequência gerada com sucesso."

    def prerequisitos_para_receita(self, receita_alvo):
        """Busca BFS reversa ou consultar dependências diretas de uma receita."""
        pass


class GrafoLogistica:
    def __init__(self):
        self.adjacencias = {}

    def adicionar_aresta(self, u, v, peso):
        if u not in self.adjacencias:
            self.adjacencias[u] = []
        if v not in self.adjacencias:
            self.adjacencias[v] = []

        self.adjacencias[u].append((v, peso))
        self.adjacencias[v].append((u, peso))

    def menor_caminho_dijkstra(self, inicio, destino):
        """Calcula a rota de entrega mais rápida."""
        distancias = {v: float('inf') for v in self.adjacencias}
        distancias[inicio] = 0
        pq = [(0, inicio)]
        caminho_anterior = {v: None for v in self.adjacencias}

        while pq:
            dist_atual, atual = heapq.heappop(pq)

            if atual == destino:
                break

            if dist_atual > distancias[atual]:
                continue

            for vizinho, peso in self.adjacencias[atual]:
                distancia_calculada = dist_atual + peso
                if distancia_calculada < distancias[vizinho]:
                    distancias[vizinho] = distancia_calculada
                    caminho_anterior[vizinho] = atual
                    heapq.heappush(pq, (distancia_calculada, vizinho))

        rota = []
        passo = destino
        while passo is not None:
            rota.append(passo)
            passo = caminho_anterior[passo]
        rota.reverse()

        return rota, distancias[destino]

    def rede_minima_prim(self, inicio):
        """Calcula a menor rede de conexões para instalar pontos operacionais."""
        visitados = set([inicio])
        arestas = []
        for vizinho, peso in self.adjacencias[inicio]:
            heapq.heappush(arestas, (peso, inicio, vizinho))

        mst = []
        custo_total = 0

        while arestas and len(visitados) < len(self.adjacencias):
            peso, u, v = heapq.heappop(arestas)
            if v not in visitados:
                visitados.add(v)
                mst.append((u, v, peso))
                custo_total += peso

                for vizinho, peso_aresta in self.adjacencias[v]:
                    if vizinho not in visitados:
                        heapq.heappush(arestas, (peso_aresta, v, vizinho))

        return mst, custo_total