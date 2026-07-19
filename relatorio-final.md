# Relatório Final: Arquitetura, Estruturas de Dados e Algoritmos

Este relatório apresenta a justificativa técnica para as estruturas de dados e os algoritmos escolhidos no desenvolvimento do sistema de gestão gastronômica. A arquitetura foi dividida em múltiplos módulos independentes, utilizando desde estruturas de busca avançada até algoritmos de otimização em grafos.

---

## 1. Módulo de Busca e Armazenamento (Catálogo de Receitas)

**Problema:** Necessidade de armazenar o cardápio e permitir buscas textuais ultrarrápidas, incluindo recurso de "autocompletar" ao digitar o nome de um prato.

### Estruturas de Dados e Algoritmos Adotados
*   **Tabela Hash (`hash.py`):** Utilizada para o armazenamento principal dos objetos das receitas. 
    *   **Justificativa:** Permite acesso direto aos dados da receita em tempo constante, complexidade de tempo médio O(1). Ideal para quando o sistema já sabe o identificador ou nome exato do prato.
*   **Árvore de Prefixos / Trie (`trie.py`):** Utilizada para a funcionalidade de busca textual e autocompletar.
    *   **Justificativa:** Diferente da Hash, a Trie permite buscas parciais (prefixos). Ao digitar "Pol", a Trie rapidamente ramifica e retorna "Polenta com Ragù". 
    *   **Complexidade:** O(L) para busca, onde L é o tamanho da palavra pesquisada, superando varreduras lineares O(N) em listas tradicionais.

---

## 2. Módulo de Produção: Linha de Montagem (Grafo de Dependências)

**Problema:** Determinar a ordem cronológica exata para preparar uma receita complexa, respeitando pré-requisitos e evitando travamentos lógicos (deadlocks) na cozinha.

### Estruturas de Dados e Algoritmos Adotados
*   **Grafo Direcionado A-cíclico (DAG):** Implementado no `grafo.py`. Representado por Lista de Adjacência e dicionário de Graus de Entrada (`in-degree`).
*   **Busca em Profundidade (DFS) via Recursão:** Lê o arquivo JSON e, no retorno da pilha de chamadas, instancia as arestas invertidas (Pré-requisito -> Receita Final).
*   **Algoritmo de Kahn (BFS / Ordenação Topológica):** Utiliza uma Fila (FIFO) para processar as receitas em camadas topológicas, partindo de vértices com grau zero.
*   **Justificativa e Complexidade:** A combinação DFS para modelagem e BFS para execução garante a geração da ordem de trabalho matematicamente perfeita em O(V + E) (onde V são as receitas e E as dependências). O Kahn também audita o grafo, garantindo que não existem dependências circulares.

---

## 3. Módulo de Logística e Entregas (Caminhos e Roteamento)

**Problema:** Calcular rotas otimizadas na malha viária urbana, tanto para entregas pontuais quanto para múltiplas entregas simultâneas.

### Estruturas de Dados e Algoritmos Adotados
*   **Grafo Ponderado Não-Direcionado:** Implementado no `grafoavancado.py`. Arestas possuem pesos que representam o custo (distância/tempo).
*   **Algoritmo de Dijkstra:**
    *   **Aplicação:** Encontrar o caminho mais curto de origem única (Restaurante -> Cliente).
    *   **Complexidade:** O((V + E) log V) utilizando uma Fila de Prioridade (Min-Heap).
*   **Problema do Caixeiro Viajante / TSP (`caixeiroviajante.py`):**
    *   **Aplicação:** Quando o entregador precisa sair do restaurante, passar por múltiplos clientes distintos na mesma viagem, e retornar à base com o menor custo total.
    *   **Justificativa:** O Dijkstra comum atende trajetos simples (A -> B), mas o módulo logístico exigia uma solução para o TSP para roteamentos complexos, garantindo economia máxima de combustível.

---

## 4. Módulo Menu VIP: Otimização com Limite de Tempo

**Problema:** Preencher um limite de tempo (ex: 55 minutos) com um conjunto de pratos que resulte na maior pontuação possível.

### Estruturas de Dados e Algoritmos Adotados
*   **Abordagem Gulosa / Greedy (`guloso.py`):** Baseado em escolhas locais, não garantem o ótimo global.
*   **Programação Dinâmica - Mochila 0/1 (`mochila01.py`):**
    *   **Estrutura:** Matriz de decisão Bottom-Up.
    *   **Justificativa:** Diferente do algoritmo guloso, a Programação Dinâmica explora subproblemas sobrepostos. A matriz O(N * W) avalia e compara todas as permutações de capacidade, garantindo matematicamente o Ótimo Global. 
    *   **Backtracking:** O algoritmo reconstrói a solução rastreando de trás para frente na matriz para identificar quais vértices (receitas) formaram a pontuação máxima.

---

## 5. Desafio Extra: Menu de Dia dos Namorados

**Problema:** Encontrar a melhor combinação exata de 1 Entrada, 1 Prato Principal e 1 Sobremesa, respeitando limites de custo e maximizando o lucro/avaliação.

### Estruturas de Dados e Algoritmos Adotados
*   **Busca Exaustiva / Força Bruta (`desafio_extra.py`):** Iteração combinatória em listas particionadas por categoria.
*   **Poda (Pruning):** Otimização que aborta laços instantaneamente caso as restrições (tempo ou orçamento) sejam violadas antes dos cálculos de mérito.
*   **Justificativa e Complexidade:** Por se tratar de um problema com restrição categórica estrita (exatamente 3 itens de categorias diferentes), não existem subproblemas sobrepostos que compensem uma matriz dinâmica. A complexidade polinomial O(E * P * S) aliada à poda condicional torna a força bruta a solução mais coesa, direta e leve para a memória neste cenário isolado.