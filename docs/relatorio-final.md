# Relatório Final - Desafio na Cozinha

## Visão Geral
O sistema foi implementado em Python com foco em três estruturas principais: tabela hash, trie e heurística gulosa. O objetivo foi reutilizar a mesma base de receitas para consulta rápida, investigação, planejamento de menus e análise logística.

## Estruturas e Justificativas

### Tabela Hash
A tabela hash foi usada para armazenar assinaturas das receitas e verificar integridade.
- Uso: comparar o estado atual de uma receita com o estado indexado em memória.
- Justificativa: acesso médio $O(1)$ para consulta de assinatura por índice.
- Complexidade:
  - inserção: $O(1)$ em média
  - verificação: $O(1)$ em média
  - auditoria geral: $O(n)$

### Trie
A trie foi usada na busca por prefixo de nomes e ingredientes.
- Uso: localizar receitas pelo início de palavras.
- Justificativa: é mais adequada que busca linear quando há consultas repetidas por prefixo.
- Complexidade:
  - inserção: $O(k)$
  - busca por prefixo: $O(k + r)$, onde $k$ é o tamanho do prefixo e $r$ o número de resultados coletados

### Heurística Gulosa
A heurística gulosa foi aplicada para recomendar menus sob restrições.
- Uso: ordenar receitas por densidade de valor e selecionar as mais vantajosas.
- Justificativa: solução simples, explicável e adequada para seleção rápida de cardápios.
- Complexidade:
  - filtragem: $O(n)$
  - ordenação: $O(n \log n)$
  - seleção: $O(n)$

## Modos Implementados

### Consulta Rápida
Permite busca por nome, categoria, ingrediente ou ID.

### Investigação
Permite:
- verificar integridade por ID
- detectar conteúdos duplicados
- detectar conflitos de versão
- validar o arquivo JSON
- detectar dependências inválidas
- identificar receitas inacessíveis
- localizar gargalos de produção
- encontrar regiões isoladas da rede

Observação: as análises de grafo usam a base de receitas e conexões por ingredientes compartilhados como proxy para a rede operacional, pois o dataset não contém uma malha de entregas real.

### Chef
Recomenda cardápios sob orçamento, tempo, dificuldade e ingredientes disponíveis.

### Logística
Avalia capacidade operacional com base em tempo médio, custo médio e carga estimada de produção.

### Menu Especial Dia dos Namorados
Seleciona automaticamente uma entrada, um prato principal e uma sobremesa dentro das restrições informadas.
- Critérios suportados: lucro, avaliação, tempo, popularidade e equilíbrio
- Saída: menu completo com justificativa e métricas agregadas

## Dados e Enriquecimento
O dataset original foi mantido, e o sistema enriquece as receitas em tempo de execução com campos derivados como:
- classe
- valor_venda
- lucro_estimado
- popularidade
- dificuldade_logistica

## Conclusão
A solução atende ao núcleo do trabalho usando estruturas de dados implementadas manualmente e reutilizando a base JSON fornecida. A parte de menu especial e investigação foi integrada ao sistema principal, sem criar uma solução separada.
