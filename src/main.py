import json
import os

from hash import TabelaHash
from trie import ArvoreTrie
from guloso import recomendar_menu_avancado
from grafo import OficinaProducao
from mochila01 import MenuVIPOtimizador
from grafoavançado import PesadeloLogistico
from caixeiroviajante import PlanejamentoEntregasTSP
from desafio_extra import MenuDiaDosNamorados

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
    dataset = carregar_dados()
    if not dataset:
        return

    receitas = dataset.get("receitas", [])
    rotas = dataset.get("rotas_logisticas", [])

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
            "4. Modo Oficina de Produção", 
            "5. Modo Menu VIP (Otimização)",
            "6. Modo Pesadelo Logístico",  
            "7. Modo Inovação do Chef (Entregas TSP)", 
            "8. Modo Especial Dia dos Namorados", 
            "0. Sair",
        ]
        print_boxed(" Desafio na Cozinha ", linhas, color_name="cyan")

        opcao = input(color("Escolha uma opção: ", "cyan"))

        if opcao == "1":
            print("\n- Consulta rápida -")
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

            print("- Modo investigação -\n")
            print("1. Verificar integridade de uma receita por ID")
            print("2. Detectar conteúdos duplicados no sistema")
            print("3. Detectar conflitos de versões de uma receita")
            print("4. Validar integridade total do arquivo JSON")

                ###########   ---   id 10 para teste
            # receita_alvo = indice_ids.get("10")
            # if receita_alvo:
            #     nome_receita = receita_alvo["nome"]
                
            #     hash_original, _ = investigador.gerar_assinatura(
            #        nome_receita, receita_alvo["ingredientes"]
            #     )

            #     ingrediente_antigo = receita_alvo["ingredientes"][0]
            #     receita_alvo["ingredientes"][0] = "Pão"

            #     hash_nova, _ = investigador.gerar_assinatura(
            #     nome_receita, receita_alvo["ingredientes"]
            #     )
                
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

        elif opcao == "4":
            print("\n- Modo Oficina de Produção -")
            oficina = OficinaProducao()

            print("[+] Carregando dependências do banco de dados...")
            for r in receitas:
                nome_dependente = r.get("nome")
                pre_requisitos = r.get("pre_requisitos", []) 
                
                oficina.adicionar_preparo(nome_dependente)
                
                for pre_req in pre_requisitos:
                    oficina.adicionar_dependencia(pre_req, nome_dependente)

            print("\n1. Qual a sequência correta para produzir o menu do dia?")
            sucesso, resultado = oficina.gerar_sequencia_producao()
            if sucesso:
                print(f" -> Sequência Válida: {resultado}")
            else:
                print(color(f" -> ERRO CRÍTICO: {resultado}", "red"))

            receita_alvo = input("\n2. Digite o nome da receita para ver seus pré-requisitos: ").strip()
            pre_reqs = oficina.listar_prerequisitos_de(receita_alvo)
            print(f" -> Pré-requisitos para {receita_alvo}: {pre_reqs}\n")

        elif opcao == "5":
            print("\n- Modo Menu Degustação VIP -")
            
            try:
                tempo_max = int(input("Tempo total disponível para o evento (minutos): "))
            except ValueError:
                print("Por favor, digite um número inteiro.")
                continue
                
            print("Critérios disponíveis: avaliacao, lucro, popularidade")
            criterio = input("O que deseja maximizar? ").strip().lower()
            
            # Validação simples
            if criterio not in ['avaliacao', 'lucro', 'popularidade']:
                criterio = 'avaliacao'
                print("Critério inválido. Usando 'avaliacao' como padrão.")

            otimizador = MenuVIPOtimizador(receitas)
            menu_vip, valor_alcancado, tempo_gasto = otimizador.otimizar_por_tempo(tempo_max, criterio)

            print_boxed(" Proposta de Menu VIP ", [
                f"Tempo Utilizado: {tempo_gasto}/{tempo_max} min",
                f"Pontuação Total ({criterio}): {valor_alcancado:.2f}"
            ],)
            
            if menu_vip:
                for prato in menu_vip:
                    print(f" -> {prato['nome']} ({prato['tempo_preparo']} min)")
            else:
                print("Nenhuma receita cabe nesse tempo!")

        elif opcao == "6":
            print("\n- Modo Pesadelo Logístico (Grafos Avançados) -")
            
            logistica = PesadeloLogistico()
            
            # Carregando do JSON dinamicamente
            for rota in rotas:
                logistica.adicionar_rota(
                    rota["origem"], 
                    rota["destino"], 
                    rota["tempo_minutos"], 
                    rota["limite_pedidos"]
                )
            
            print("\n1. Menor Rede de Conexões (Kruskal - MST)")
            print("Objetivo: Interligar todos os pontos operacionais com o menor custo/tempo.")
            rede, custo = logistica.calcular_menor_infraestrutura()
            for u, v, peso in rede:
                print(f"Instalar conexão: {u} <-> {v} (Custo: {peso})")
            print(f"Custo Total Mínimo da Infraestrutura: {custo}\n")
            
            print("2. Rotas e Estimativas de Tempo (Dijkstra)")
            
            # Deixando dinâmico para o usuário escolher a rota!
            origem_busca = input("Digite o ponto de origem (ex: Cozinha Matriz): ").strip()
            destino_busca = input("Digite o destino (ex: Bairro Nobre): ").strip()
            
            caminho, tempo = logistica.calcular_rota_mais_rapida(origem_busca, destino_busca)
            if caminho:
                print(f"   -> Rota Sugerida: {' -> '.join(caminho)}")
                print(f"   => Tempo Estimado: {tempo} minutos\n")
            else:
                print("   -> Rota inatingível ou pontos não cadastrados.\n")
            
            print("3. Capacidade Máxima e Gargalos (Edmonds-Karp)")
            print(f"Objetivo: Quantos pedidos simultâneos podem ir de {origem_busca} para {destino_busca}?")
            capacidade = logistica.calcular_capacidade_maxima(origem_busca, destino_busca)
            print(f"   => Capacidade Simultânea Máxima: {capacidade} pedidos\n")

        elif opcao == "7":
            print("\n- Modo Inovação do Chef (Múltiplas Entregas - TSP) -")
            
            # Carregando a malha logística silenciosamente para o TSP poder usar
            logistica = PesadeloLogistico()
            for rota in rotas:
                logistica.adicionar_rota(rota["origem"], rota["destino"], rota["tempo_minutos"], rota["limite_pedidos"])
            
            tsp = PlanejamentoEntregasTSP(logistica)
            
            # 1. Pegando a origem de forma dinâmica
            origem = input("Digite o ponto de partida do entregador (ex: Cozinha Matriz): ").strip().title()
            
            # 2. Pegando os múltiplos destinos de forma dinâmica
            print("\nDigite os bairros de entrega separados por vírgula.")
            entrada_bairros = input("Ex (Bairro Nobre, Bairro Industrial, Bairro Centro): ")
            
            # 3. Tratamento de dados: separa por vírgula, tira espaços em branco e arruma as maiúsculas
            bairros_para_visitar = [b.strip().title() for b in entrada_bairros.split(",") if b.strip()]
            
            if not bairros_para_visitar:
                print(color("   -> Erro: Você não digitou nenhum bairro válido.\n", "red"))
                continue
            
            print(f"\nO entregador sairá da(o) {origem}.")
            print(f"Ele precisa entregar pedidos nos seguintes locais: {', '.join(bairros_para_visitar)}")

            # 4. Chama o algoritmo com as listas dinâmicas
            melhor_rota, menor_tempo = tsp.calcular_rota_tsp_exata(origem, bairros_para_visitar)
            
            if melhor_rota:
                print(f"\n   -> Sequência Ótima de Entrega:")
                print(f"      {' -> '.join(melhor_rota)}")
                print(f"   -> Tempo Total no trânsito (ida e volta): {menor_tempo} minutos\n")
            else:
                print("   -> Erro: Não é possível visitar todos esses bairros (rota inatingível).\n")
        elif opcao == "8":
            print("\n- Modo Especial Dia dos Namorados -")
            try:
                tempo_max = int(input("Tempo máximo de preparo (minutos): ").strip())
                custo_max = float(input("Custo limite para o menu (R$): ").strip())
                
                print("Objetivo de otimização (digite o número):")
                print("1. Maior Lucro")
                print("2. Melhor Avaliação Média")
                print("3. Menor Tempo de Preparo")
                escolha_obj = input("Opção: ").strip()
                
                mapa_objetivos = {"1": "lucro", "2": "avaliacao", "3": "tempo"}
                objetivo = mapa_objetivos.get(escolha_obj, "lucro")

                # Instancia a classe passando a lista de receitas carregada do JSON
                gerador_menu = MenuDiaDosNamorados(receitas)
                melhor_menu = gerador_menu.selecionar_melhor_menu(tempo_max, custo_max, objetivo)
                
                if melhor_menu:
                    print(color("\nMenu Especial Dia dos Namorados:", "cyan"))
                    print(f"Entrada: {melhor_menu['entrada']}")
                    print(f"Prato principal: {melhor_menu['principal']}")
                    print(f"Sobremesa: {melhor_menu['sobremesa']}\n")
                    print(f"Valor total de venda: R$ {melhor_menu['valor_venda']:.2f}")
                    print(f"Custo estimado: R$ {melhor_menu['custo_total']:.2f}")
                    print(f"Lucro estimado: R$ {melhor_menu['lucro_total']:.2f}")
                    print(f"Tempo total de preparo: {melhor_menu['tempo_total']} minutos")
                    print(f"Avaliação média: {melhor_menu['avaliacao_media']}")
                    print(f"Dificuldade logística: {melhor_menu['dificuldade_logistica']}\n")
                    
                    # Justificativa simples
                    print("Justificativa:")
                    print(f"O menu foi escolhido por otimizar o critério de '{objetivo}' dentro dos limites de custo (R$ {custo_max:.2f}) e tempo ({tempo_max} min).")
                else:
                    print(color("\n-> Não foi possível encontrar um menu que atenda a essas restrições.", "red"))

            except ValueError:
                print(color("-> Erro: Digite valores numéricos válidos para tempo e custo.", "red"))

        elif opcao == "0":
            print("Encerrando.")
            break


if __name__ == "__main__":
    main()
