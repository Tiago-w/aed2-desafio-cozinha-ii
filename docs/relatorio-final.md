# Relatório Final - Desafio na Cozinha

## Visão Geral
O sistema foi implementado em Python e evoluiu de um simples buscador para um **Sistema de Gestão (ERP)** completo. O projeto engloba oito módulos operacionais, transitando por estruturas primárias (Tabelas Hash e Tries), algoritmos heurísticos (Gulosos), otimização exata (Programação Dinâmica), análise de redes (Grafos Básicos e Avançados) e combinatória (Força Bruta e Backtracking). 

A arquitetura garante que a mesma base de dados (agora ramificada entre catálogo de receitas e malha logística) seja consumida e processada por diferentes paradigmas algorítmicos.

---

## Estruturas e Justificativas

### 1. Tabela Hash e Árvore Trie (Módulos 1 e 2)
A tabela hash foi implementada manualmente para o armazenamento principal e verificação de integridade, enquanto a Trie foi utilizada para buscas textuais.
*   **Justificativa:** A Hash garante resgate e auditoria em tempo constante, ideal para chamadas de sistema através de IDs (como feito no módulo do Dia dos Namorados). A Trie elimina a necessidade de varredura linear em consultas textuais iterativas.
*   **Complexidades (Hash):** Inserção/Busca média em $O(1)$; Auditoria geral em $O(n)$.
*   **Complexidades (Trie):** Inserção em $O(k)$; Busca por prefixo em $O(k + r)$, onde $k$ é o tamanho do prefixo e $r$ o volume de resultados.

### 2. Heurística Gulosa / Greedy (Módulo 3)
Aplicada para recomendar menus rápidos sob restrições orçamentárias.
*   **Justificativa:** Oferece uma solução subótima, porém extremamente rápida e explicável para a tomada de decisão no salão do restaurante, baseando-se na densidade de valor (Avaliação/Custo).
*   **Complexidades:** Filtragem em $O(n)$; Ordenação em $O(n \log n)$; Seleção em $O(n)$.

### 3. Programação Dinâmica (Módulo 5)
Implementação do *Problema da Mochila 0/1* para a elaboração de Menus VIPs.
*   **Justificativa:** Diferente da heurística gulosa, a Programação Dinâmica garante matematicamente o lucro máximo absoluto dentro de um limite de tempo estrito, sem desperdiçar capacidade de produção.
*   **Complexidade:** $O(n \cdot W)$, onde $n$ é o número de receitas e $W$ é o tempo limite da cozinha.

### 4. Teoria dos Grafos (Módulos 4 e 6)
O sistema modelou duas redes distintas: a árvore de dependências da cozinha e a rede de entregas.
*   **Justificativa e Algoritmos:** 
    *   **Busca em Largura (BFS) / Kahn:** Usado para ordenação topológica dos pré-requisitos das receitas na "Oficina de Produção". Complexidade: $O(V + E)$.
    *   **Kruskal (MST):** Calcula a infraestrutura de rede mais barata para interligar filiais. Complexidade: $O(E \log V)$.
    *   **Dijkstra:** Define rotas de entrega de menor tempo/custo. Complexidade: $O(E \log V)$.
    *   **Edmonds-Karp (Max Flow):** Identifica gargalos e a capacidade máxima simultânea de envio de pedidos. Complexidade: $O(V E^2)$.

### 5. Força Bruta e Permutação (Módulos 7 e 8)
Usada para resolver o Problema do Caixeiro Viajante (TSP) e o Produto Cartesiano de cardápios.
*   **Justificativa:** Para problemas NP-Difíceis com um $N$ pequeno (ex: 3 a 5 bairros de entrega, ou a montagem de um combo de 3 pratos), a busca exaustiva (Backtracking) roda em milissegundos e garante a resposta perfeita sem a necessidade de heurísticas de aproximação complexas.
*   **Complexidades:** TSP roda em $O(V!)$; O Produto Cartesiano do menu roda em $O(E \times P \times S)$ (Entradas $\times$ Principais $\times$ Sobremesas).

---

## Modos Implementados (Funcionalidades)

1.  **Consulta Rápida:** Busca instantânea por nome, categoria, ingrediente ou ID.
2.  **Investigação:** Módulo de auditoria para integridade, duplicidade e invalidação de dependências do banco de dados.
3.  **Chef:** Recomendação de cardápios rápidos via heurística gulosa.
4.  **Oficina de Produção:** Organização da linha de montagem e ordem de preparo das receitas.
5.  **Menu VIP:** Maximização de lucro sob restrição de tempo da cozinha (Mochila 0/1).
6.  **Pesadelo Logístico:** Análise completa da rede de delivery (Kruskal, Dijkstra e Edmonds-Karp).
7.  **Inovação do Chef (Entregas TSP):** Planejamento inteligente de múltiplas entregas encontrando o ciclo de menor custo para o entregador.
8.  **Menu Especial Dia dos Namorados:** Sistema de apoio à decisão que avalia milhares de combinações para selecionar automaticamente o melhor trio (Entrada, Principal e Sobremesa) com base no critério de otimização escolhido (lucro, avaliação ou tempo), respeitando os limites da cozinha e conectando os resultados com a Tabela Hash.

---

## Dados e Enriquecimento
O arquivo JSON estático (`dataset.json`) sofreu uma reformulação arquitetural para suportar a complexidade do sistema. Ele agora abriga duas raízes de dados independentes:
*   **Catálogo de Receitas:** Mantém a estrutura original de fichas técnicas.
*   **Rotas Logísticas:** Uma malha vetorial de arestas (origem, destino, tempo, capacidade) que reflete a rede de entregas real do restaurante.

Ademais, o sistema enriquece as instâncias em memória durante o tempo de execução, calculando dinamicamente campos como `lucro_estimado`, `classe` e proporção de `custo_benefício`.

---

## Conclusão
A solução entregue atende a todos os requisitos e desafios extras da disciplina. O sistema comprova que estruturas clássicas implementadas do zero (sem uso de bibliotecas terceiras para o núcleo algorítmico) podem ser perfeitamente integradas para resolver problemas complexos de gestão empresarial, tomada de decisão e análise logística de forma fluida e escalável.