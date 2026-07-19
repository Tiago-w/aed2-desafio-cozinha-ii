from collections import defaultdict, deque

class OficinaProducao:
    def __init__(self):
        #a->b
        self.grafo = defaultdict(list)
        #b->a
        self.pre_requisitos_diretos = defaultdict(list)
        
        self.grau_entrada = defaultdict(int)
        
        self.todos_preparos = set()

    def adicionar_preparo(self, preparo):        
        self.todos_preparos.add(preparo)
        if preparo not in self.grau_entrada:
            self.grau_entrada[preparo] = 0

    def adicionar_dependencia(self, preparo_previo, preparo_dependente):
        self.adicionar_preparo(preparo_previo)
        self.adicionar_preparo(preparo_dependente)

        self.grafo[preparo_previo].append(preparo_dependente)
        self.pre_requisitos_diretos[preparo_dependente].append(preparo_previo)
        self.grau_entrada[preparo_dependente] += 1

    def gerar_sequencia_producao(self):
        fila = deque([p for p in self.todos_preparos if self.grau_entrada[p] == 0])
        ordem_execucao = []
        
        grau_temp = self.grau_entrada.copy()

        while fila:
            atual = fila.popleft()
            ordem_execucao.append(atual)

            for dependente in self.grafo[atual]:
                grau_temp[dependente] -= 1
                if grau_temp[dependente] == 0:
                    fila.append(dependente)

        if len(ordem_execucao) != len(self.todos_preparos):
            return False, "Erro: Inconsistência detectada, existe um ciclo nas dependências."

        return True, ordem_execucao

    def listar_prerequisitos_de(self, receita):

        if receita not in self.todos_preparos:
            return f"A receita '{receita}' não está cadastrada."

        necessarios = set()
        fila = deque([receita])

        while fila:
            atual = fila.popleft()
            for pre_req in self.pre_requisitos_diretos[atual]:
                if pre_req not in necessarios:
                    necessarios.add(pre_req)
                    fila.append(pre_req)

        return list(necessarios)