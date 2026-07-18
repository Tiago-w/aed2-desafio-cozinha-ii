# Sistema de Gestão: Desafio na Cozinha

![Python](https://img.shields.io/badge/Linguagem-Python-blue.svg)
![Estruturas](https://img.shields.io/badge/Estruturas-Hash%20%7C%20Trie%20%7C%20Grafos%20%7C%20DP-success.svg)
![Status](https://img.shields.io/badge/Status-Concluído-warning.svg)

Sistema de gerenciamento de acervo culinário e gestão logística desenvolvido para otimizar operações de busca, planejamento de cardápios e roteamento de entregas sob restrições. O sistema utiliza um **banco de dados em formato JSON (dataset estático)**, contendo tanto as fichas técnicas das receitas quanto a malha de rotas de delivery.

As receitas são enriquecidas em tempo de execução com campos auxiliares para a tomada de decisão, como `classe`, `valor_venda`, `popularidade`, `lucro_estimado` e `dificuldade_logistica`.

---

## Desenvolvedores
* **Tiago Wolowski**
* **Gustavo Serratte**

---

## Arquitetura e Estruturas de Dados

O projeto evoluiu para um sistema de gestão completo (ERP), integrando múltiplas estruturas e paradigmas algorítmicos:

* **Banco de Dados:** Utiliza o formato **JSON** para armazenamento de receitas e malha logística.
* **Tabela Hash:** Implementada para armazenamento primário (O(1)) e resgate rápido de entidades usando IDs.
* **Árvore Trie:** Busca rápida de prefixos para autocompletar nomes e ingredientes.
* **Algoritmos Gulosos (Greedy):** Motor de recomendação heurística visando custo-benefício.
* **Programação Dinâmica (DP):** Solução exata para o Problema da Mochila 0/1 na criação de Menus VIPs otimizados.
* **Grafos Básicos e Avançados:** 
  * **Busca em Largura (BFS) / Ordenação Topológica:** Para organizar a ordem de preparo e os pré-requisitos das receitas.
  * **Algoritmo de Kruskal (MST):** Para calcular a infraestrutura de rede mais barata.
  * **Algoritmo de Dijkstra:** Para definir a rota de entrega mais rápida.
  * **Edmonds-Karp (Max Flow):** Para calcular gargalos e a capacidade máxima simultânea da cozinha.
* **Força Bruta e Backtracking:** Resolução exata de permutações e Produto Cartesiano para o Caixeiro Viajante (TSP) e o Desafio de Dia dos Namorados.

---

## Modos do Sistema (Funcionalidades)

1. **Modo Consulta Rápida:** Busca por nome, categoria, ingrediente ou ID.
2. **Modo Investigação:** Auditoria de integridade, identificação de dependências inválidas e gargalos de produção.
3. **Modo Chef:** Recomendação gulosa sob orçamento, tempo e dificuldade.
4. **Modo Oficina de Produção:** Organiza a linha de montagem e dependências entre receitas (Grafos).
5. **Modo Menu VIP:** Otimização matemática (DP) para maximizar o lucro de um menu dentro de um tempo limite.
6. **Modo Pesadelo Logístico:** Análise da rede de delivery, incluindo rotas (Dijkstra), gargalos de capacidade (Max Flow) e custos de infraestrutura (Kruskal).
7. **Modo Inovação do Chef (Múltiplas Entregas):** Planejamento inteligente de rotas usando o Problema do Caixeiro Viajante (TSP) para encontrar o ciclo Hamiltoniano de menor custo.
8. **Modo Especial Dia dos Namorados:** Tomada de decisão sob restrições via Produto Cartesiano integrado à Tabela Hash, selecionando automaticamente o melhor trio (Entrada, Principal e Sobremesa) otimizado por lucro, avaliação ou tempo.

---

## [RECUPERAÇÃO P1]
* **Questão Escolhida:** Algoritmos Gulosos (Heurística baseada no Problema da Mochila 0/1).

* **Explicação Arquitetural:** O sistema implementa uma abordagem gulosa (Greedy) para recomendar um menu otimizado. O processo ocorre em três etapas:

* **Filtragem Rígida:** Elimina opções que ultrapassem as restrições fixas do usuário (orçamento máximo, tempo de preparo individual ou dificuldade específica).

* **Cálculo de Densidade:** Uma nota de prioridade (Avaliação ou Popularidade) é dividida pelo Custo ou pelo Tempo, dependendo do objetivo ("economico" ou "rapido"), criando uma proporção de custo-benefício.

* **Seleção Gulosa:** As receitas são ordenadas de forma decrescente por essa densidade. O algoritmo itera sobre a lista incluindo os itens mais vantajosos no menu, empilhando-os até que o limite orçamentário (`orcamento_maximo`) seja atingido.

--- 

## Estrutura do Projeto
* `data/`: `dataset.json` (Banco de dados contendo o dicionário de receitas e rotas logísticas).
* `src/`: Código-fonte (Implementação de todas as estruturas e da lógica dos 8 módulos).
* `docs/`: Documentação extra e relatórios teóricos de modelagem.

---

## Guia de Execução

### Pré-requisitos
* Python 3.x nativo (Nenhuma biblioteca externa de estruturas de dados foi utilizada para o núcleo do sistema).

### Inicialização
Para iniciar o menu interativo no console, execute:
```bash
python src/main.py