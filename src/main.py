import json
import os

from hash import TabelaHash
from trie import ArvoreTrie
from guloso import recomendar_menu_avancado

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

    while True:
        linhas = [
            "1. Modo Consulta Rápida",
            "2. Modo Investigação",
            "3. Modo Chef",
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
                cat = input(
                    "Digite a categoria (entrada/principal/sobremesa): "
                ).lower()
                res = [r["nome"] for r in receitas if r.get("categoria") == cat]
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

            print("Modo investigação\n")
            print("1. Verificar integridade de uma receita por ID")
            print("2. Detectar conteúdos duplicados no sistema")
            print("3. Detectar conflitos de versões de uma receita")
            print("4. Validar integridade total do arquivo JSON")

                ###########   ---   id 10 para teste
            # receita_alvo = indice_ids.get("10")
            # if receita_alvo:
            #     nome_receita = receita_alvo["nome"]
                
            #    ## hash_original, _ = investigador.gerar_assinatura(
            #    ##     nome_receita, receita_alvo["ingredientes"]
            #    ##  )

            #     ingrediente_antigo = receita_alvo["ingredientes"][0]
            #     receita_alvo["ingredientes"][0] = "Pão"

            #     # hash_nova, _ = investigador.gerar_assinatura(
            #     # nome_receita, receita_alvo["ingredientes"]
            #     #     )
            #     
                ############
            sub_opcao = input("Escolha a verificação: ")

            if sub_opcao == "1":


                id_verificar = input(
                    "Digite o ID da receita para checar (tente o ID 10): "
                ).strip()
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

        elif opcao == "0":
            print("Encerrando.")
            break


if __name__ == "__main__":
    main()
