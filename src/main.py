import json
import os

from hash import TabelaHash
from trie import ArvoreTrie
from guloso import recomendar_menu_avancado, recomendar_menu_namorados
from grafo import GrafoDependencias, GrafoLogistica


def carregar_grafo_producao(receitas):
    grafo = GrafoDependencias()
    for r in receitas:
        grafo.adicionar_receita(r['id'])
        if 'dependencias' in r:
            for dep in r['dependencias']:
                grafo.adicionar_dependencia(dep, r['id'])
    return grafo

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


def carregar_dados():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(caminho_atual, "..", "data", "dataset.json")

    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Ficheiro de base de dados não encontrado em {caminho_arquivo}.")
        return []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    receitas = carregar_dados()
    if not receitas:
        return

    investigador = TabelaHash(tamanho_inicial=20)
    busca_rapida = ArvoreTrie()
    indice_ids = {}

    for r in receitas:
        id_receita, nome, ingredientes = (
            r.get("id"),
            r.get("nome"),
            r.get("ingredientes"),
        )
        if not id_receita or not nome or not ingredientes:
            continue

        investigador.inserir(id_receita, nome, ingredientes)

        indice_ids[id_receita] = r

        busca_rapida.inserir(nome, id_receita)
        for palavra in nome.split():
            busca_rapida.inserir(palavra, id_receita)

    grafo_producao = carregar_grafo_producao(receitas)

    while True:
        linhas = [
            "1. Consulta Rápida",
            "2. Investigação e Produção (Mód 5)",
            "3. O Chef Responde (Mód 6)",
            "4. Logística Delivery (Mód 7)",
            "5. Especial Dia dos Namorados",
            "6. Laboratório (Inovação - Mód 8)",
            "0. Sair",
        ]
        print_boxed(" Desafio na Cozinha ", linhas, color_name="cyan")
        opcao = input(color("Escolha uma opção: ", "cyan"))

        if opcao == "1":
            print("\nConsulta rápida")
            print("A) Por Nome | B) Por Categoria | C) Por Ingrediente | D) Por ID")
            sub_op = input("Escolha o filtro: ").upper()

            if sub_op == "A":
                termo = input("Digite o nome ou parte dele: ")
                ids = busca_rapida.buscar_prefixo(termo)
                print(
                    f"Receitas encontradas: {[indice_ids[i]['nome'] for i in ids] if ids else 'Nenhuma.'}"
                )
            elif sub_op == "B":
                cat = input("Digite a categoria (entrada/principal/sobremesa): ").lower()
                res = [r["nome"] for r in receitas if r.get("categoria").lower() == cat]
                print(f"Receitas da categoria '{cat}': {res}")
            elif sub_op == "C":
                ing = input("Digite o ingrediente: ").lower()
                res = [
                    r["nome"]
                    for r in receitas
                    if any(ing in i.lower() for i in r.get("ingredientes", []))
                ]
                print(f"Receitas contendo '{ing}': {res}")
            elif sub_op == "D":
                id_busca = input("Digite o ID único (ex: 01): ").upper()
                receita = indice_ids.get(id_busca)
                print(
                    f"Resultado: {receita['nome']} (Custo: R${receita['custo_estimado']})"
                    if receita
                    else "ID não encontrado."
                )

        elif opcao == "2":
            print("\n- Modo Investigação e Produção -")
            print("--- Integridade (T1) ---")
            print("1. Verificar integridade de uma receita por ID")
            print("2. Detectar conteúdos duplicados no sistema")
            print("3. Detectar conflitos de versões de uma receita")
            print("4. Validar integridade total do arquivo JSON")
            print("--- Oficina de Produção (Módulo 5) ---")
            print("5. Gerar sequência correta de produção (Ordenação Topológica)")
            print("6. Verificar se existem erros de dependência (Ciclos)")

            sub_opcao = input("Escolha uma opção: ")

            if sub_opcao == "1":
                id_verificar = input("Digite o ID da receita para checar: ").strip()
                r = indice_ids.get(id_verificar)
                if r:
                    status = investigador.verificar_integridade(r["id"], r["nome"], r["ingredientes"])
                    print(f"-> Receita '{r['nome']}': {'Íntegra' if status else 'Alterada'}")
                else:
                    print("Código de receita inexistente.")

            elif sub_opcao == "2":
                duplicados, _ = investigador.auditoria_de_duplicados_e_conflitos()
                print("\nProcurando receitas com conteudo duplicado:")
                if duplicados:
                    for ass, lista in duplicados.items():
                        print(f" -> Alerta: Mesmo conteúdo compartilhado por IDs: {lista}")
                else:
                    print("Nenhuma receita com conteúdo duplicado foi encontrada.")

            elif sub_opcao == "3":
                _, conflitos = investigador.auditoria_de_duplicados_e_conflitos()
                if conflitos:
                    for nome_conflito, registros in conflitos.items():
                        print(f" -> Conflito detectado na receita '{nome_conflito.upper()}':")
                        for id_rec, ass in registros:
                            print(f"    * ID: {id_rec} | Assinatura: {ass}")
                else:
                    print("Nenhum conflito de versão detectado.")

            elif sub_opcao == "4":
                violacoes = sum(1 for r in receitas if not investigador.verificar_integridade(r["id"], r["nome"], r["ingredientes"]))
                if violacoes == 0:
                    print("Sucesso: todos os dados batem com a Tabela Hash.")
                else:
                    print(f"Auditoria concluída: {violacoes} adulterações encontradas.")
            
            elif sub_opcao == "5":
                ordem, mensagem = grafo_producao.gerar_ordem_producao()
                if ordem:
                    nomes_ordem = [indice_ids[i]['nome'] for i in ordem if i in indice_ids]
                    print(color("\nSequência de Produção Sugerida:", "green"))
                    print(" -> ".join(nomes_ordem))
                else:
                    print(color(f"\n{mensagem}", "red"))

            elif sub_opcao == "6":
                ordem, mensagem = grafo_producao.gerar_ordem_producao()
                if ordem is None:
                    print(color(f"\nAlerta Crítico: {mensagem}", "red"))
                    print("Não é possível cozinhar o menu devido a um loop nas dependências!")
                else:
                    print(color("\nNenhum erro de dependência. O cardápio é viável!", "green"))
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
                print("\nLendo arquivo e comprando com a hash")

                violacoes = 0
                for r in receitas:
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

        elif opcao == "3":
            print("\n- Modo chefe  -")
            orcamento = float(input("Orçamento Máximo (R$): ") or "999")
            tempo = float(input("Tempo Máximo (minutos): ") or "999")
            objetivo = input("Objetivo do Menu (economico / rapido): ").lower()
            prioridade = input("Priorizar por (avaliacao / popularidade): ").lower()

            restricoes = {"orcamento_maximo": orcamento, "tempo_maximo": tempo}
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
            print("\n- Logística Delivery -")
            caminho_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "logistica.json")
            if not os.path.exists(caminho_mapa):
                print("Erro: logistica.json não encontrado. Rode o script gerar_mapa.py primeiro.")
                continue

            with open(caminho_mapa, "r") as f:
                dados_mapa = json.load(f)

            grafo_mapa = GrafoLogistica()
            for u, v, peso in dados_mapa['arestas']:
                grafo_mapa.adicionar_aresta(u, v, peso)

            print("A) Calcular Rota mais rápida (Dijkstra)")
            print("B) Expandir infraestrutura de Cozinhas (Árvore Geradora Mínima - Prim)")
            sub = input("Opção: ").upper()

            if sub == "A":
                origem = input("Ponto de Origem (Ex: Ponto_1): ")
                destino = input("Ponto de Destino (Ex: Ponto_30): ")
                try:
                    rota, tempo = grafo_mapa.menor_caminho_dijkstra(origem, destino)
                    print(f"\nRota mais rápida: {' -> '.join(rota)}")
                    print(f"Tempo estimado da viagem: {tempo} minutos")
                except Exception:
                    print("Ponto não encontrado no sistema.")

            elif sub == "B":
                mst, custo = grafo_mapa.rede_minima_prim("Ponto_1")
                print(f"\nPara interligar todas as cozinhas e bairros, o custo/distância mínima será: {custo}")
                print(f"Conexões a construir: {len(mst)} ruas essenciais.")

        elif opcao == "5":
            print("\n- Menu Especial Dia dos Namorados -")
            orc = float(input("Orçamento Máximo de Custo (R$): ") or "100")
            tmp = float(input("Tempo Máximo de Preparo (minutos): ") or "120")

            menu_namorados = recomendar_menu_namorados(receitas, {'orcamento_maximo': orc, 'tempo_maximo': tmp})
            if menu_namorados:
                print(color("\nSugestão do Chef para o Dia dos Namorados:", "magenta"))
                print(f"-> Entrada: {menu_namorados['entrada']['nome']}")
                print(f"-> Principal: {menu_namorados['principal']['nome']}")
                print(f"-> Sobremesa: {menu_namorados['sobremesa']['nome']}")
                print(f"\nLucro Estimado do Menu: R$ {menu_namorados['lucro']:.2f}")
                print(f"Avaliação Média Geral: {menu_namorados['avaliacao_media']:.1f}")
                print(f"Tempo Total: {menu_namorados['tempo_total']} min")
                print(color("\nJustificativa:", "yellow"))
                print("O menu foi escolhido por maximizar a relação entre o lucro estimado")
                print("e a avaliação média dos clientes, respeitando os limites de tempo e orçamento,")
                print("garantindo que no máximo um prato possua dificuldade logística 'alta'.")
            else:
                print("A cozinha não consegue produzir um menu completo viável com essas restrições!")

        elif opcao == "6":
            print("\n- Laboratório de Inovação: Comunidades Gastronômicas -")
            print("Analisando famílias de receitas ligadas por dependências...")
            familias = grafo_producao.identificar_comunidades()
            if familias:
                for idx, familia in enumerate(familias, 1):
                    nomes = [indice_ids[i]['nome'] for i in familia if i in indice_ids]
                    print(f"Família {idx}: {nomes}")
            else:
                print("Não foram encontradas famílias conexas.")

        elif opcao == "0":
            print("Encerrando a cozinha. Au revoir!")
            break


if __name__ == "__main__":
    main()
