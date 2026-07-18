from collections import defaultdict, deque

class OficinaProducao:
    def __init__(self):
        # grafo: mapeia um preparo para os preparos que dependem dele (A -> B)
        self.grafo = defaultdict(list)
        
        # pre_requisitos: mapeia um preparo para os que ele precisa (B -> A)
        self.pre_requisitos_diretos = defaultdict(list)
        
        # grau_entrada: conta quantas dependências um preparo tem antes de ser iniciado
        self.grau_entrada = defaultdict(int)
        
        self.todos_preparos = set()

    def adicionar_preparo(self, preparo):
        """Garante que o preparo exista no sistema."""
        self.todos_preparos.add(preparo)
        if preparo not in self.grau_entrada:
            self.grau_entrada[preparo] = 0

    def adicionar_dependencia(self, preparo_previo, preparo_dependente):
        """Define que 'preparo_previo' deve ser feito antes de 'preparo_dependente'."""
        self.adicionar_preparo(preparo_previo)
        self.adicionar_preparo(preparo_dependente)

        self.grafo[preparo_previo].append(preparo_dependente)
        self.pre_requisitos_diretos[preparo_dependente].append(preparo_previo)
        self.grau_entrada[preparo_dependente] += 1

    # --- CONSULTA 1 & 2: Menu do Dia e Inconsistências ---
    def gerar_sequencia_producao(self):
        """
        Retorna uma tupla (sucesso, resultado).
        Se sucesso for True, resultado é a lista com a ordem de preparo.
        Se sucesso for False, resultado é a mensagem de erro (ciclo detectado).
        """
        # Fila começa com preparos que não dependem de ninguém (grau de entrada == 0)
        fila = deque([p for p in self.todos_preparos if self.grau_entrada[p] == 0])
        ordem_execucao = []
        
        # Cópia para não alterar o estado original durante a consulta
        grau_temp = self.grau_entrada.copy()

        while fila:
            atual = fila.popleft()
            ordem_execucao.append(atual)

            # Para cada preparo dependente, "resolvemos" uma dependência
            for dependente in self.grafo[atual]:
                grau_temp[dependente] -= 1
                # Se todas as dependências foram resolvidas, entra na fila
                if grau_temp[dependente] == 0:
                    fila.append(dependente)

        # Se a ordem não contiver todos os preparos, há um ciclo (inconsistência)
        if len(ordem_execucao) != len(self.todos_preparos):
            return False, "Erro crítico: Inconsistência detectada! Existe um ciclo nas dependências."

        return True, ordem_execucao

    # --- CONSULTA 3: Preparos antes da Receita X ---
    def listar_prerequisitos_de(self, receita):
        """
        Retorna todos os preparos que precisam estar prontos (direta ou indiretamente)
        antes de iniciar a receita informada.
        """
        if receita not in self.todos_preparos:
            return f"A receita '{receita}' não está cadastrada."

        necessarios = set()
        fila = deque([receita])

        # Busca em Largura (BFS) reversa
        while fila:
            atual = fila.popleft()
            for pre_req in self.pre_requisitos_diretos[atual]:
                if pre_req not in necessarios:
                    necessarios.add(pre_req)
                    fila.append(pre_req)

        return list(necessarios)