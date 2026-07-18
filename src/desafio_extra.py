class MenuDiaDosNamorados:
    def __init__(self, receitas):
        # Filtra as receitas por categoria
        self.entradas = [r for r in receitas if r.get("categoria", "").lower() == "entrada"]
        self.principais = [r for r in receitas if r.get("categoria", "").lower() == "principal"]
        self.sobremesas = [r for r in receitas if r.get("categoria", "").lower() == "sobremesa"]

    def selecionar_melhor_menu(self, tempo_max, custo_max, objetivo="lucro"):
        """
        Gera combinações, filtra pelas restrições e retorna o melhor menu com base no objetivo.
        Objetivos válidos: 'lucro', 'avaliacao', 'tempo'
        """
        melhor_menu = None
        melhor_pontuacao = -float('inf') if objetivo in ["lucro", "avaliacao"] else float('inf')

        # Força Bruta para testar todas as combinações de 3 pratos (Produto Cartesiano)
        for entrada in self.entradas:
            for principal in self.principais:
                for sobremesa in self.sobremesas:
                    
                    custo_total = entrada["custo_estimado"] + principal["custo_estimado"] + sobremesa["custo_estimado"]
                    tempo_total = entrada["tempo_preparo"] + principal["tempo_preparo"] + sobremesa["tempo_preparo"]
                    
                    # Filtra: descarta menus que violam as restrições
                    if custo_total > custo_max or tempo_total > tempo_max:
                        continue
                    
                    # Calcula as métricas do menu candidato
                    lucro_total = entrada["lucro"] + principal["lucro"] + sobremesa["lucro"]
                    avaliacao_media = round((entrada["avaliacao"] + principal["avaliacao"] + sobremesa["avaliacao"]) / 3, 2)
                    valor_venda = custo_total + lucro_total

                    # Define a pontuação baseada no objetivo
                    if objetivo == "lucro":
                        pontuacao_atual = lucro_total
                    elif objetivo == "avaliacao":
                        pontuacao_atual = avaliacao_media
                    elif objetivo == "tempo":
                        pontuacao_atual = tempo_total
                    else:
                        pontuacao_atual = lucro_total # Default

                    # Atualiza o melhor menu encontrado
                    is_melhor = (pontuacao_atual > melhor_pontuacao) if objetivo in ["lucro", "avaliacao"] else (pontuacao_atual < melhor_pontuacao)
                    
                    if is_melhor:
                        melhor_pontuacao = pontuacao_atual
                        melhor_menu = {
                            "entrada": entrada["nome"],
                            "principal": principal["nome"],
                            "sobremesa": sobremesa["nome"],
                            "custo_total": custo_total,
                            "lucro_total": lucro_total,
                            "valor_venda": valor_venda,
                            "tempo_total": tempo_total,
                            "avaliacao_media": avaliacao_media,
                            "dificuldade_logistica": "Média" # Fixo para simplificação, pode ser adaptado
                        }

        return melhor_menu