def recomendar_menu_avancado(receitas, restricoes, objetivo="economico", prioridade="avaliacao"):
    receitas_validas = []

    for receita in receitas:
        custo = receita.get('custo_estimado', 0)
        tempo = receita.get('tempo_preparo', 0)

        if custo > restricoes.get('orcamento_maximo', float('inf')):
            continue
        if tempo > restricoes.get('tempo_maximo', float('inf')):
            continue
        if restricoes.get('dificuldade') and receita.get('dificuldade') != restricoes['dificuldade']:
            continue

        valor_base = receita.get('avaliacao', 0) if prioridade == "avaliacao" else receita.get('popularidade')

        if objetivo == "economico":
            densidade = valor_base / custo if custo > 0 else 0
            justificativa = f"Excelente densidade de {prioridade} por Custo (R${custo:.2f})."
        elif objetivo == "rapido":
            densidade = valor_base / tempo if tempo > 0 else 0
            justificativa = f"Excelente densidade de {prioridade} por Tempo de Preparo ({tempo} min)."
        else:
            densidade = valor_base
            justificativa = f"Valor base de {prioridade}: {valor_base}"

        r_enriquecida = receita.copy()
        r_enriquecida['densidade'] = densidade
        r_enriquecida['justificativa'] = justificativa
        receitas_validas.append(r_enriquecida)

    receitas_ordenadas = sorted(receitas_validas, key=lambda x: x['densidade'], reverse=True)

    menu_recomendado = []
    custo_total = 0.0
    tempo_total = 0

    for receita in receitas_ordenadas:
        if custo_total + receita.get('custo_estimado', 0) <= restricoes.get('orcamento_maximo', float('inf')):
            menu_recomendado.append(receita)
            custo_total += receita.get('custo_estimado', 0)
            tempo_total += receita.get('tempo_preparo', 0)

    return menu_recomendado, custo_total, tempo_total