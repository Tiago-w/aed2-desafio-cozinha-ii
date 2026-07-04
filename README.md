# Sistema de Gestão: Desafio na Cozinha

![Python](https://img.shields.io/badge/Linguagem-Python-blue.svg)
![Estruturas](https://img.shields.io/badge/Estruturas-Hash%20%7C%20Trie%20%7C%20Guloso-success.svg)
![Status](https://img.shields.io/badge/Status-Concluído-warning.svg)

Sistema de gerenciamento de acervo culinário desenvolvido para otimizar operações de busca, organização de ingredientes e recomendação de menus sob restrições. O sistema utiliza um **banco de dados em formato JSON (dataset estático)**, permitindo portabilidade e fácil manipulação dos dados de receitas.

As receitas são enriquecidas em tempo de execução com campos auxiliares para a tomada de decisão, como `classe`, `valor_venda`, `popularidade`, `lucro_estimado` e `dificuldade_logistica`.

---

## Desenvolvedores
* **Tiago Wolowski**
* **Gustavo Serratte**

---

## Arquitetura e Estruturas de Dados

* **Banco de Dados:** Utiliza o formato **JSON** para armazenamento persistente e leitura dinâmica dos dados, garantindo uma estrutura hierárquica eficiente para ingredientes e passos de preparo.
* **Tabela Hash:** Implementada manualmente para armazenamento primário e verificação de integridade.
* **Árvore Trie:** Implementada manualmente para busca rápida de prefixos (nomes e ingredientes).
* **Algoritmo Guloso:** Motor de recomendação baseado no Problema da Mochila 0/1, otimizando cardápios via densidade de valor ($V_i/C_i$).

---

## Modos do Sistema

* **Consulta Rápida:** busca por nome, categoria, ingrediente ou ID.
* **Investigação:** auditoria de integridade, duplicidade e conflitos de versão.
* **Chef:** recomendação gulosa sob orçamento, tempo, dificuldade e disponibilidade de ingredientes.
* **Logística:** análise operacional com foco em capacidade, tempo médio e carga de produção.
* **Menu Especial Dia dos Namorados:** seleção de uma entrada, um prato principal e uma sobremesa com base em restrições e critério de otimização.

---


## [RECUPERAÇÃO P1]
* **Questão Escolhida:** Algoritmos Gulosos (Heurística baseada no Problema da Mochila 0/1).

* **Explicação Arquitetural:** O sistema implementa uma abordagem gulosa (Greedy) para recomendar um menu otimizado. O processo ocorre em três etapas:

* **Filtragem Rígida:** Elimina opções que ultrapassem as restrições fixas do usuário (orçamento máximo, tempo de preparo individual ou dificuldade específica).

* **Cálculo de Densidade:** Uma nota de prioridade (Avaliação ou Popularidade) é dividida pelo Custo ou pelo Tempo, dependendo do objetivo ("economico" ou "rapido"), criando uma proporção de custo-benefício.

* **Seleção Gulosa:** As receitas são ordenadas de forma decrescente por essa densidade. O algoritmo itera sobre a lista incluindo os itens mais vantajosos no menu, empilhando-os até que o limite orçamentário (orcamento_maximo) seja atingido.


--- 


## Estrutura do Projeto
* `data/`: `dataset.json` (Banco de dados de receitas).
* `src/`: Código-fonte (Implementação das estruturas e lógica principal).
* `docs/`: Documentação extra.

---

## Guia de Execução

### Pré-requisitos
* Python 3.x

### Inicialização
```bash
py src/main.py
```

### Observação
O menu especial utiliza a base de receitas existente e calcula automaticamente os campos auxiliares necessários para comparar as combinações válidas.

### Link do repositório:
* [https://github.com/Tiago-w/aed2-desafio-cozinha.git](https://github.com/Tiago-w/aed2-desafio-cozinha.git)
