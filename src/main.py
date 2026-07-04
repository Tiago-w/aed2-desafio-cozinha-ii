import json
import os

from hash import TabelaHash
from trie import ArvoreTrie
from guloso import (
    analisar_componentes_ingredientes,
    analisar_dependencias_invalidas,
    analisar_logistica,
    analisar_gargalos_producao,
    analisar_receitas_inacessiveis,
    preparar_cardapio,
    recomendar_menu_avancado,
    recomendar_menu_especial,
)

# saída colorida e caixas com bordas
try:
    from colorama import init as _init_colorama, Fore, Style

    _init_colorama(autoreset=True)
    _COLORS = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "reset": Style.RESET_ALL,
    }
except Exception:
    _COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
    }


def color(text, name="reset"):
    return f"{_COLORS.get(name, '')}{text}{_COLORS.get('reset','')}"


import re


def _strip_ansi(s: str) -> str:
    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_re.sub("", s)


def print_boxed(title, lines, color_name="cyan"):
    visible_width = max(len(title), *(len(_strip_ansi(l)) for l in lines)) + 4
    top = "┌" + "─" * (visible_width - 2) + "┐"
    sep = "├" + "─" * (visible_width - 2) + "┤"
    bottom = "└" + "─" * (visible_width - 2) + "┘"
    print(color(top, color_name))
    print(color(f"│ {title.center(visible_width-4)} │", color_name))
    print(color(sep, color_name))
    for l in lines:
        pad = visible_width - 4 - len(_strip_ansi(l))
        print(color(f"│ {l}{' ' * pad} │", color_name))
    print(color(bottom, color_name))


#################################################################


def _normalizar_lista(texto):
    if not texto:
        return []
    return [item.strip() for item in texto.split(",") if item.strip()]


def _imprimir_receita(receita):
    print(
        f"-> {receita.get('nome', '?')} | R$ {float(receita.get('valor_venda', 0)):.2f}"
        f" | Custo R$ {float(receita.get('custo_estimado', 0)):.2f}"
        f" | Lucro R$ {float(receita.get('lucro_estimado', 0)):.2f}"
        f" | {float(receita.get('tempo_preparo', 0)):.0f} min"
    )


def _imprimir_menu_especial(menu, metricas):
    print_boxed(
        "Menu Especial Dia dos Namorados",
        [
            f"Entrada: {menu[0].get('nome', '?')}",
            f"Prato principal: {menu[1].get('nome', '?')}",
            f"Sobremesa: {menu[2].get('nome', '?')}",
            f"Valor total de venda: R$ {metricas['valor_total_venda']:.2f}",
            f"Custo estimado: R$ {metricas['custo_total']:.2f}",
            f"Lucro estimado: R$ {metricas['lucro_total']:.2f}",
            f"Tempo total de preparo: {metricas['tempo_total']:.0f} min",
            f"Avaliação média: {metricas['avaliacao_media']:.2f}",
            f"Popularidade média: {metricas['popularidade_media']:.2f}",
            f"Dificuldade logística média: {metricas['dificuldade_media']:.2f}",
        ],
        color_name="magenta",
    )


def _imprimir_logistica(resultado):
    receitas = resultado["receitas_filtradas"]
    print_boxed(
        "Modo Logística",
        [
            f"Receitas analisadas: {len(receitas)}",
            f"Tempo médio: {resultado['tempo_medio']:.2f} min",
            f"Custo médio: R$ {resultado['custo_medio']:.2f}",
            f"Capacidade estimada na janela informada: {resultado['capacidade_estimada']} receitas",
        ],
        color_name="yellow",
    )

    if not receitas:
        print("Nenhuma receita passou nas restrições logísticas informadas.")
        return

    print("\nReceitas com menor carga operacional:")
    for receita in receitas[:5]:
        print(
            f"- {receita.get('nome', '?')} | {receita.get('classe', '?')} | "
            f"{receita.get('dificuldade_logistica', '?')} | {float(receita.get('tempo_preparo', 0)):.0f} min"
        )


def _imprimir_resultado_lista(titulo, itens):
    print_boxed(titulo, [f"Total: {len(itens)}"], color_name="red")
    if not itens:
        print("Nenhum resultado encontrado.")
        return

    for item in itens:
        if isinstance(item, dict):
            detalhes = []
            for chave, valor in item.items():
                if chave == "nome":
                    continue
                detalhes.append(f"{chave}: {valor}")
            print(f"- {item.get('nome', '?')} | {' | '.join(detalhes)}")
        else:
            print(f"- {item}")


def carregar_dados():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(caminho_atual, "..", "data", "dataset.json")

    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Ficheiro de base de dados não encontrado em {caminho_arquivo}.")
        return []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    receitas_base = carregar_dados()
    if not receitas_base:
        return

    receitas = preparar_cardapio(receitas_base)
    investigador = TabelaHash(tamanho_inicial=20)
    busca_rapida = ArvoreTrie()
    indice_ids = {r["id"]: r for r in receitas}

    for r in receitas_base:
        id_receita = r.get("id")
        nome = r.get("nome")
        ingredientes = r.get("ingredientes")
        if not id_receita or not nome or not ingredientes:
            continue

        investigador.inserir(id_receita, nome, ingredientes)

        busca_rapida.inserir(nome, id_receita)
        for palavra in nome.split():
            busca_rapida.inserir(palavra, id_receita)
        for ingrediente in ingredientes:
            for palavra in ingrediente.split():
                busca_rapida.inserir(palavra, id_receita)

    while True:
        linhas = [
            "1. Modo Consulta Rápida",
            "2. Modo Investigação",
            "3. Modo Chef",
            "4. Modo Logística",
            "5. Menu Especial Dia dos Namorados",
            "0. Sair",
        ]
        print_boxed(" Desafio na Cozinha ", linhas, color_name="cyan")

        opcao = input(color("Escolha uma opção: ", "cyan")).strip()

        if opcao == "1":
            print("\nConsulta rápida")
            print("A) Por Nome | B) Por Categoria | C) Por Ingrediente | D) Por ID")
            sub_op = input("Escolha o filtro: ").strip().upper()

            if sub_op == "A":
                termo = input("Digite o nome ou parte dele: ").strip()
                ids = busca_rapida.buscar_prefixo(termo)
                nomes = [indice_ids[i]["nome"] for i in ids if i in indice_ids]
                print(f"Receitas encontradas: {nomes if nomes else 'Nenhuma.'}")
            elif sub_op == "B":
                cat = input(
                    "Digite a categoria (entrada/principal/sobremesa): "
                ).strip().lower()
                mapa_categorias = {
                    "entrada": "entrada",
                    "principal": "prato principal",
                    "prato principal": "prato principal",
                    "sobremesa": "sobremesa",
                }
                classe = mapa_categorias.get(cat, cat)
                res = [r["nome"] for r in receitas if r.get("classe") == classe]
                print(f"Receitas da categoria '{cat}': {res}")
            elif sub_op == "C":
                ing = input("Digite o ingrediente: ").strip().lower()
                res = [
                    r["nome"]
                    for r in receitas
                    if any(ing in i.lower() for i in r.get("ingredientes", []))
                ]
                print(f"Receitas contendo '{ing}': {res}")
            elif sub_op == "D":
                id_busca = input("Digite o ID único (ex: 01): ").strip().upper()
                receita = indice_ids.get(id_busca)
                print(
                    f"Resultado: {receita['nome']} (Custo: R$ {receita['custo_estimado']:.2f}, Valor de venda: R$ {receita['valor_venda']:.2f})"
                    if receita
                    else "ID não encontrado."
                )

        elif opcao == "2":
            print("Modo investigação\n")
            print("1. Verificar integridade de uma receita por ID")
            print("2. Detectar conteúdos duplicados no sistema")
            print("3. Detectar conflitos de versões de uma receita")
            print("4. Validar integridade total do arquivo JSON")
            print("5. Detectar dependências inválidas")
            print("6. Identificar receitas inacessíveis")
            print("7. Localizar gargalos de produção")
            print("8. Encontrar regiões isoladas da rede")
            sub_opcao = input("Escolha a verificação: ").strip()

            if sub_opcao == "1":
                id_verificar = input(
                    "Digite o ID da receita para checar (tente o ID 10): "
                ).strip().upper()
                r = indice_ids.get(id_verificar)

                if r:
                    status = investigador.verificar_integridade(
                        r["id"], r["nome"], r["ingredientes"]
                    )
                    print(f"-> Receita '{r['nome']}': {'Íntegra' if status else 'Alterado'}")
                else:
                    print("Código de receita inexistente.")

            elif sub_opcao == "2":
                duplicados, _ = investigador.auditoria_de_duplicados_e_conflitos()
                print("\nProcurando receitas com conteudo duplicado:")
                if duplicados:
                    for ass, lista in duplicados.items():
                        print(
                            f" -> Alerta: Mesmo conteúdo compartilhado por IDs diferentes: {lista}"
                        )
                else:
                    print("Nenhuma receita com conteúdo duplicado foi encontrada.")

            elif sub_opcao == "3":
                _, conflitos = investigador.auditoria_de_duplicados_e_conflitos()
                print(
                    "\nDetectando conflitos de versões (Mesmo nome, conteúdos diferentes):"
                )
                if conflitos:
                    for nome_conflito, registros in conflitos.items():
                        print(
                            f" -> Conflito detectado na receita '{nome_conflito.upper()}':"
                        )
                        for id_rec, ass in registros:
                            print(f"    * ID: {id_rec} | Assinatura de Conteúdo: {ass}")
                else:
                    print("Nenhuma inconsistência ou conflito de versão detectado.")

            elif sub_opcao == "4":
                print("\nLendo arquivo e comparando com a hash")
                
                violacoes = 0
                for r in receitas_base:
                    if not investigador.verificar_integridade(
                        r["id"], r["nome"], r["ingredientes"]
                    ):
                        print(
                            f"Violação de integridade: A receita ID {r['id']} foi alterada em disco"
                        )
                        violacoes += 1
                if violacoes == 0:
                    print(
                        "Sucesso, todos os dados em disco batem com o snapshot da Tabela Hash."
                    )
                else:
                    print(f"Auditoria concluída: {violacoes} adulterações encontradas.")
            elif sub_opcao == "5":
                ingredientes_validos = _normalizar_lista(
                    input(
                        "Lista de ingredientes válidos disponíveis (separados por vírgula, opcional): "
                    ).strip().lower()
                )
                dependencias = analisar_dependencias_invalidas(receitas, ingredientes_validos)
                resultado = [
                    {
                        "nome": indice_ids[id_receita]["nome"],
                        "id": id_receita,
                        "faltantes": faltantes,
                    }
                    for id_receita, faltantes in dependencias.items()
                ]
                _imprimir_resultado_lista("Dependências inválidas", resultado)
            elif sub_opcao == "6":
                ingredientes_validos = _normalizar_lista(
                    input("Lista de ingredientes disponíveis (separados por vírgula): ").strip().lower()
                )
                inacessiveis = analisar_receitas_inacessiveis(receitas, ingredientes_validos)
                _imprimir_resultado_lista("Receitas inacessíveis", inacessiveis)
            elif sub_opcao == "7":
                gargalos = analisar_gargalos_producao(receitas)
                _imprimir_resultado_lista("Gargalos de produção", gargalos)
            elif sub_opcao == "8":
                componentes = analisar_componentes_ingredientes(receitas)
                print_boxed("Regiões isoladas da rede", [f"Total de componentes: {len(componentes)}"], color_name="red")
                for indice, componente in enumerate(componentes, start=1):
                    print(f"- Componente {indice}: {componente}")
        elif opcao == "3":
            print("\n- Modo chefe  -")
            orcamento = float(input("Orçamento Máximo (R$): ") or "999")
            tempo = float(input("Tempo Máximo (minutos): ") or "999")
            objetivo = input("Objetivo do menu (economico / rapido / lucro / equilibrio): ").strip().lower()
            prioridade = input("Priorizar por (avaliacao / popularidade): ").strip().lower()
            dificuldade = input("Dificuldade logística máxima (baixa / media / alta, opcional): ").strip().lower()
            ingredientes_disponiveis = _normalizar_lista(
                input("Ingredientes disponíveis para este menu (separados por vírgula, opcional): ").strip().lower()
            )

            restricoes = {"orcamento_maximo": orcamento, "tempo_maximo": tempo}
            if dificuldade:
                restricoes["dificuldade"] = dificuldade
            if ingredientes_disponiveis:
                restricoes["ingredientes_disponiveis"] = ingredientes_disponiveis

            menu, custo_f, tempo_f = recomendar_menu_avancado(
                receitas, restricoes, objetivo, prioridade
            )

            print("\n Menu Recomendado:")
            if menu:
                for p in menu:
                    print(
                        f"-> {p.get('nome','?')} | R$ {p.get('custo_estimado',0)} | {p.get('tempo_preparo','?')}min"
                    )
                    print(f"   Justificativa: {p.get('justificativa','-')}")
                print(f"Total: R$ {custo_f:.2f} | Tempo Estimado: {tempo_f} min")
            else:
                print("Nenhuma sugestão de menu foi gerada.")

        elif opcao == "4":
            print("\n- Modo Logística  -")
            orcamento = float(input("Orçamento Máximo (R$): ") or "999")
            tempo = float(input("Tempo Máximo por janela de operação (minutos): ") or "999")
            dificuldade = input("Dificuldade logística máxima (baixa / media / alta, opcional): ").strip().lower()
            capacidade = float(input("Capacidade da cozinha em carga operacional (padrão 999): ") or "999")
            ingredientes_disponiveis = _normalizar_lista(
                input("Ingredientes disponíveis para a operação (separados por vírgula, opcional): ").strip().lower()
            )

            restricoes = {
                "orcamento_maximo": orcamento,
                "tempo_maximo": tempo,
                "capacidade_cozinha": capacidade,
            }
            if dificuldade:
                restricoes["dificuldade"] = dificuldade
            if ingredientes_disponiveis:
                restricoes["ingredientes_disponiveis"] = ingredientes_disponiveis

            resultado = analisar_logistica(receitas, restricoes)
            _imprimir_logistica(resultado)

        elif opcao == "5":
            print("\n- Menu Especial Dia dos Namorados  -")
            orcamento = float(input("Orçamento Máximo do menu (R$): ") or "999")
            tempo = float(input("Tempo Máximo total (minutos): ") or "999")
            capacidade = float(input("Capacidade máxima da cozinha em carga operacional (padrão 999): ") or "999")
            dificuldade = input("Dificuldade logística máxima (baixa / media / alta, opcional): ").strip().lower()
            ingredientes_disponiveis = _normalizar_lista(
                input("Ingredientes disponíveis para o menu (separados por vírgula, opcional): ").strip().lower()
            )
            objetivo = input(
                "Critério de otimização (lucro / avaliacao / tempo / popularidade / equilibrio): "
            ).strip().lower() or "equilibrio"
            prioridade = input("Priorizar por (avaliacao / popularidade): ").strip().lower() or "avaliacao"

            restricoes = {
                "orcamento_maximo": orcamento,
                "tempo_maximo": tempo,
                "capacidade_cozinha": capacidade,
                "dificuldade_logistica": dificuldade,
                "ingredientes_disponiveis": ingredientes_disponiveis,
            }

            menu, metricas = recomendar_menu_especial(receitas, restricoes, objetivo, prioridade)

            if menu:
                metricas["valor_total_venda"] = sum(float(item.get("valor_venda") or 0) for item in menu)
                _imprimir_menu_especial(menu, metricas)
                print(f"Justificativa: {metricas['justificativa']}")
            else:
                print(
                    "Nenhum menu completo foi encontrado dentro das restrições informadas. "
                    f"Combinações válidas: {metricas['combinacoes_validas']} de {metricas['total_combinacoes']}."
                )

        elif opcao == "0":
            print("Encerrando.")
            break


if __name__ == "__main__":
    main()
