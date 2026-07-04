from itertools import product
from collections import defaultdict, deque


def _normalizar_texto(valor):
    return str(valor or "").strip().lower()


def _normalizar_ingredientes(ingredientes):
    return {_normalizar_texto(item) for item in (ingredientes or []) if _normalizar_texto(item)}


def classificar_receita(receita):
    categoria = _normalizar_texto(receita.get("categoria"))
    tipo = _normalizar_texto(receita.get("tipo de prato") or receita.get("tipo_de_prato"))

    if "entrada" in categoria or "entrada" in tipo:
        return "entrada"
    if "sobremesa" in categoria or "sobremesa" in tipo:
        return "sobremesa"
    return "prato principal"


def _converter_dificuldade_logistica(receita):
    valor = receita.get("dificuldade_logistica")
    if isinstance(valor, (int, float)):
        if valor <= 1:
            return "baixa", 1
        if valor == 2:
            return "media", 2
        if valor >= 3:
            return "alta", 3

    texto = _normalizar_texto(valor)
    if texto in {"baixa", "baixo", "facil", "fácil", "leve"}:
        return "baixa", 1
    if texto in {"media", "média", "medio", "médio", "moderada", "moderado"}:
        return "media", 2
    if texto in {"alta", "alto", "dificil", "difícil", "complexa", "complexo"}:
        return "alta", 3

    tempo = float(receita.get("tempo_preparo") or 0)
    quantidade_ingredientes = len(receita.get("ingredientes") or [])
    custo = float(receita.get("custo_estimado") or 0)
    score = (tempo / 30.0) + (quantidade_ingredientes / 4.0) + (custo / 40.0)

    if score < 3.2:
        return "baixa", 1
    if score < 5.0:
        return "media", 2
    return "alta", 3


def enriquecer_receita(receita):
    receita_enriquecida = receita.copy()
    custo = float(receita_enriquecida.get("custo_estimado") or 0)
    tempo = float(receita_enriquecida.get("tempo_preparo") or 0)
    avaliacao = float(receita_enriquecida.get("avaliacao") or 0)

    classe = classificar_receita(receita_enriquecida)
    dificuldade_texto, dificuldade_score = _converter_dificuldade_logistica(receita_enriquecida)

    valor_venda = receita_enriquecida.get("valor_venda")
    if valor_venda is None:
        margem = 1.35 + (avaliacao / 10.0)
        valor_venda = round(custo * margem, 2)
    else:
        valor_venda = float(valor_venda)

    popularidade = receita_enriquecida.get("popularidade")
    if popularidade is None:
        popularidade = round(
            max(0.0, min(100.0, (avaliacao * 18.0) + (50.0 - custo * 0.25) - (tempo * 0.05))),
            2,
        )
    else:
        popularidade = float(popularidade)

    receita_enriquecida["classe"] = classe
    receita_enriquecida["valor_venda"] = valor_venda
    receita_enriquecida["lucro_estimado"] = round(valor_venda - custo, 2)
    receita_enriquecida["popularidade"] = popularidade
    receita_enriquecida["dificuldade_logistica"] = dificuldade_texto
    receita_enriquecida["dificuldade_logistica_score"] = dificuldade_score
    return receita_enriquecida


def preparar_cardapio(receitas):
    return [enriquecer_receita(receita) for receita in receitas]


def construir_grafo_ingredientes(receitas):
    receitas_enriquecidas = [enriquecer_receita(receita) for receita in receitas]
    grafo = {receita["id"]: set() for receita in receitas_enriquecidas}
    ingredientes_por_receita = {
        receita["id"]: _normalizar_ingredientes(receita.get("ingredientes")) for receita in receitas_enriquecidas
    }

    ids = list(grafo.keys())
    for indice, id_origem in enumerate(ids):
        ingredientes_origem = ingredientes_por_receita[id_origem]
        for id_destino in ids[indice + 1 :]:
            if ingredientes_origem & ingredientes_por_receita[id_destino]:
                grafo[id_origem].add(id_destino)
                grafo[id_destino].add(id_origem)

    return grafo, ingredientes_por_receita, receitas_enriquecidas


def analisar_dependencias_invalidas(receitas, ingredientes_validos=None):
    ingredientes_validos = _normalizar_ingredientes(ingredientes_validos)
    receitas_enriquecidas = [enriquecer_receita(receita) for receita in receitas]
    mapa_ingredientes = defaultdict(list)

    for receita in receitas_enriquecidas:
        for ingrediente in receita.get("ingredientes") or []:
            mapa_ingredientes[_normalizar_texto(ingrediente)].append(receita["id"])

    dependencias_invalidas = {}
    if ingredientes_validos:
        for receita in receitas_enriquecidas:
            faltantes = [
                ingrediente
                for ingrediente in receita.get("ingredientes") or []
                if _normalizar_texto(ingrediente) not in ingredientes_validos
            ]
            if faltantes:
                dependencias_invalidas[receita["id"]] = faltantes
    else:
        for receita in receitas_enriquecidas:
            raros = [
                ingrediente
                for ingrediente in receita.get("ingredientes") or []
                if len(mapa_ingredientes[_normalizar_texto(ingrediente)]) == 1
            ]
            if raros:
                dependencias_invalidas[receita["id"]] = raros

    return dependencias_invalidas


def analisar_componentes_ingredientes(receitas):
    grafo, _, receitas_enriquecidas = construir_grafo_ingredientes(receitas)
    visitados = set()
    componentes = []
    mapa_nome = {receita["id"]: receita["nome"] for receita in receitas_enriquecidas}

    for no_inicio in grafo:
        if no_inicio in visitados:
            continue

        fila = deque([no_inicio])
        componente = []
        visitados.add(no_inicio)

        while fila:
            no_atual = fila.popleft()
            componente.append(no_atual)
            for vizinho in grafo[no_atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        componentes.append([mapa_nome[id_receita] for id_receita in componente])

    componentes.sort(key=len, reverse=True)
    return componentes


def analisar_gargalos_producao(receitas):
    grafo, _, receitas_enriquecidas = construir_grafo_ingredientes(receitas)
    grau = {id_receita: len(vizinhos) for id_receita, vizinhos in grafo.items()}
    mapa_nome = {receita["id"]: receita for receita in receitas_enriquecidas}

    ordenados = sorted(grau.items(), key=lambda item: (item[1], -float(mapa_nome[item[0]].get("tempo_preparo") or 0)), reverse=True)
    gargalos = []
    for id_receita, grau_receita in ordenados[:5]:
        receita = mapa_nome[id_receita]
        gargalos.append(
            {
                "id": id_receita,
                "nome": receita.get("nome", "?"),
                "grau": grau_receita,
                "tempo_preparo": receita.get("tempo_preparo", 0),
                "custo_estimado": receita.get("custo_estimado", 0),
            }
        )

    return gargalos


def analisar_receitas_inacessiveis(receitas, ingredientes_disponiveis):
    ingredientes_disponiveis = _normalizar_ingredientes(ingredientes_disponiveis)
    receitas_enriquecidas = [enriquecer_receita(receita) for receita in receitas]
    inacessiveis = []

    for receita in receitas_enriquecidas:
        ingredientes = _normalizar_ingredientes(receita.get("ingredientes"))
        if ingredientes and not ingredientes.issubset(ingredientes_disponiveis):
            inacessiveis.append(
                {
                    "id": receita["id"],
                    "nome": receita.get("nome", "?"),
                    "faltantes": sorted(ingredientes - ingredientes_disponiveis),
                }
            )

    return inacessiveis


def _valor_base_receita(receita, prioridade):
    prioridade = _normalizar_texto(prioridade)
    if prioridade == "popularidade":
        return float(receita.get("popularidade") or 0)
    if prioridade == "lucro":
        return float(receita.get("lucro_estimado") or 0)
    return float(receita.get("avaliacao") or 0)


def recomendar_menu_avancado(receitas, restricoes, objetivo="economico", prioridade="avaliacao"):
    receitas_validas = []
    orcamento_maximo = float(restricoes.get("orcamento_maximo", float("inf")))
    tempo_maximo = float(restricoes.get("tempo_maximo", float("inf")))
    dificuldade_maxima = _normalizar_texto(restricoes.get("dificuldade"))
    limite_dificuldade = {"baixa": 1, "media": 2, "média": 2, "alta": 3}.get(dificuldade_maxima)
    ingredientes_disponiveis = {
        _normalizar_texto(item) for item in restricoes.get("ingredientes_disponiveis", []) if item
    }

    for receita in receitas:
        receita_enriquecida = enriquecer_receita(receita)
        custo = float(receita_enriquecida.get("custo_estimado") or 0)
        tempo = float(receita_enriquecida.get("tempo_preparo") or 0)

        if custo > orcamento_maximo:
            continue
        if tempo > tempo_maximo:
            continue
        if limite_dificuldade is not None and receita_enriquecida.get("dificuldade_logistica_score", 3) > limite_dificuldade:
            continue
        if ingredientes_disponiveis:
            ingredientes = {_normalizar_texto(item) for item in receita_enriquecida.get("ingredientes") or []}
            if not ingredientes.issubset(ingredientes_disponiveis):
                continue

        valor_base = _valor_base_receita(receita_enriquecida, prioridade)

        if objetivo == "economico":
            densidade = valor_base / custo if custo > 0 else 0
            justificativa = f"Boa relação de {prioridade} por custo (R$ {custo:.2f})."
        elif objetivo == "rapido":
            densidade = valor_base / tempo if tempo > 0 else 0
            justificativa = f"Boa relação de {prioridade} por tempo de preparo ({tempo:.0f} min)."
        elif objetivo == "lucro":
            densidade = float(receita_enriquecida.get("lucro_estimado") or 0)
            justificativa = f"Maior lucro estimado entre as opções válidas (R$ {densidade:.2f})."
        else:
            densidade = valor_base
            justificativa = f"Valor base de {prioridade}: {valor_base:.2f}."

        receita_enriquecida["densidade"] = densidade
        receita_enriquecida["justificativa"] = justificativa
        receitas_validas.append(receita_enriquecida)

    receitas_ordenadas = sorted(
        receitas_validas,
        key=lambda item: (item["densidade"], item.get("avaliacao", 0), -item.get("tempo_preparo", 0)),
        reverse=True,
    )

    menu_recomendado = []
    custo_total = 0.0
    tempo_total = 0.0

    for receita in receitas_ordenadas:
        novo_custo_total = custo_total + float(receita.get("custo_estimado") or 0)
        novo_tempo_total = tempo_total + float(receita.get("tempo_preparo") or 0)
        if novo_custo_total <= orcamento_maximo and novo_tempo_total <= tempo_maximo:
            menu_recomendado.append(receita)
            custo_total = novo_custo_total
            tempo_total = novo_tempo_total

    return menu_recomendado, custo_total, tempo_total


def _validar_combo(combo, restricoes):
    custo_total = sum(float(receita.get("custo_estimado") or 0) for receita in combo)
    tempo_total = sum(float(receita.get("tempo_preparo") or 0) for receita in combo)
    orcamento_maximo = float(restricoes.get("orcamento_maximo", float("inf")))
    tempo_maximo = float(restricoes.get("tempo_maximo", float("inf")))
    dificuldade_maxima = _normalizar_texto(restricoes.get("dificuldade_logistica"))
    capacidade_cozinha = float(restricoes.get("capacidade_cozinha", float("inf")))
    ingredientes_disponiveis = {
        _normalizar_texto(item) for item in restricoes.get("ingredientes_disponiveis", []) if item
    }

    if custo_total > orcamento_maximo or tempo_total > tempo_maximo:
        return False

    carga_operacional = 0.0
    for receita in combo:
        if dificuldade_maxima:
            limite = {"baixa": 1, "media": 2, "alta": 3}.get(dificuldade_maxima, 3)
            if receita.get("dificuldade_logistica_score", 3) > limite:
                return False

        if ingredientes_disponiveis:
            ingredientes = {_normalizar_texto(item) for item in receita.get("ingredientes") or []}
            if not ingredientes.issubset(ingredientes_disponiveis):
                return False

        carga_operacional += float(receita.get("tempo_preparo") or 0) + (len(receita.get("ingredientes") or []) * 2)

    return carga_operacional <= capacidade_cozinha


def _pontuar_menu(combo, objetivo, prioridade):
    custo_total = sum(float(receita.get("custo_estimado") or 0) for receita in combo)
    tempo_total = sum(float(receita.get("tempo_preparo") or 0) for receita in combo)
    lucro_total = sum(float(receita.get("lucro_estimado") or 0) for receita in combo)
    avaliacao_media = sum(float(receita.get("avaliacao") or 0) for receita in combo) / len(combo)
    popularidade_media = sum(float(receita.get("popularidade") or 0) for receita in combo) / len(combo)
    dificuldade_media = sum(float(receita.get("dificuldade_logistica_score") or 0) for receita in combo) / len(combo)

    objetivo = _normalizar_texto(objetivo)
    prioridade = _normalizar_texto(prioridade)
    valor_prioridade = avaliacao_media if prioridade == "avaliacao" else popularidade_media

    if objetivo == "lucro":
        score = lucro_total * 2.0 + valor_prioridade
    elif objetivo == "avaliacao":
        score = avaliacao_media * 25.0 + lucro_total * 0.25
    elif objetivo == "tempo":
        score = (1000.0 - tempo_total) + valor_prioridade * 5.0
    elif objetivo == "popularidade":
        score = popularidade_media * 20.0 + lucro_total * 0.15
    else:
        score = (
            lucro_total * 1.4
            + avaliacao_media * 12.0
            + popularidade_media * 0.35
            - tempo_total * 0.45
            - dificuldade_media * 6.0
        )

    return {
        "score": score,
        "custo_total": custo_total,
        "tempo_total": tempo_total,
        "lucro_total": lucro_total,
        "avaliacao_media": avaliacao_media,
        "popularidade_media": popularidade_media,
        "dificuldade_media": dificuldade_media,
    }


def recomendar_menu_especial(receitas, restricoes, objetivo="equilibrio", prioridade="avaliacao"):
    receitas_enriquecidas = [enriquecer_receita(receita) for receita in receitas]
    por_classe = {"entrada": [], "prato principal": [], "sobremesa": []}

    for receita in receitas_enriquecidas:
        classe = receita.get("classe")
        if classe in por_classe:
            por_classe[classe].append(receita)

    melhor_combo = None
    melhor_metricas = None
    total_combinacoes = 0
    combinacoes_validas = 0

    for combo in product(por_classe["entrada"], por_classe["prato principal"], por_classe["sobremesa"]):
        total_combinacoes += 1
        if not _validar_combo(combo, restricoes):
            continue

        combinacoes_validas += 1
        metricas = _pontuar_menu(combo, objetivo, prioridade)

        if melhor_metricas is None or metricas["score"] > melhor_metricas["score"]:
            melhor_combo = combo
            melhor_metricas = metricas
        elif melhor_metricas is not None and metricas["score"] == melhor_metricas["score"]:
            if (metricas["tempo_total"], metricas["custo_total"]) < (
                melhor_metricas["tempo_total"],
                melhor_metricas["custo_total"],
            ):
                melhor_combo = combo
                melhor_metricas = metricas

    if melhor_combo is None:
        return None, {
            "total_combinacoes": total_combinacoes,
            "combinacoes_validas": combinacoes_validas,
        }

    nome_objetivo = _normalizar_texto(objetivo)
    if nome_objetivo == "lucro":
        justificativa = "O menu foi escolhido por oferecer o maior lucro estimado entre as combinações válidas."
    elif nome_objetivo == "avaliacao":
        justificativa = "O menu foi escolhido por entregar a melhor avaliação média dentro das restrições informadas."
    elif nome_objetivo == "tempo":
        justificativa = "O menu foi escolhido por reduzir o tempo total de preparo sem violar orçamento ou capacidade."
    elif nome_objetivo == "popularidade":
        justificativa = "O menu foi escolhido por concentrar a maior popularidade média entre as opções viáveis."
    else:
        justificativa = "O menu foi escolhido por equilibrar lucro, avaliação, popularidade, tempo e complexidade logística."

    justificativa += (
        f" Foram analisadas {total_combinacoes} combinações e {combinacoes_validas} passaram nas restrições."
    )

    menu = list(melhor_combo)
    for receita in menu:
        receita["justificativa"] = justificativa

    melhor_metricas["justificativa"] = justificativa
    return menu, melhor_metricas


def analisar_logistica(receitas, restricoes):
    receitas_enriquecidas = [enriquecer_receita(receita) for receita in receitas]
    max_tempo = float(restricoes.get("tempo_maximo", float("inf")))
    max_custo = float(restricoes.get("orcamento_maximo", float("inf")))
    nivel_maximo = _normalizar_texto(restricoes.get("dificuldade"))

    filtradas = []
    for receita in receitas_enriquecidas:
        if float(receita.get("tempo_preparo") or 0) > max_tempo:
            continue
        if float(receita.get("custo_estimado") or 0) > max_custo:
            continue
        if nivel_maximo:
            limite = {"baixa": 1, "media": 2, "alta": 3}.get(nivel_maximo, 3)
            if receita.get("dificuldade_logistica_score", 3) > limite:
                continue
        filtradas.append(receita)

    filtradas.sort(
        key=lambda receita: (
            receita.get("dificuldade_logistica_score", 3),
            receita.get("tempo_preparo", 0),
            -receita.get("popularidade", 0),
        )
    )

    tempo_medio = sum(float(item.get("tempo_preparo") or 0) for item in filtradas) / len(filtradas) if filtradas else 0
    custo_medio = sum(float(item.get("custo_estimado") or 0) for item in filtradas) / len(filtradas) if filtradas else 0
    capacidade_estimada = int(max_tempo // tempo_medio) if tempo_medio else 0

    return {
        "receitas_filtradas": filtradas,
        "tempo_medio": round(tempo_medio, 2),
        "custo_medio": round(custo_medio, 2),
        "capacidade_estimada": capacidade_estimada,
    }