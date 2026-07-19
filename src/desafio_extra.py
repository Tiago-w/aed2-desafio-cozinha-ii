class MenuDiaDosNamorados:
    def __init__(self, receitas):
        # Filtra as receitas por categoria
        self.entradas = [r for r in receitas if r.get("categoria", "").lower() == "entrada"]
        self.principais = [r for r in receitas if r.get("categoria", "").lower() == "principal"]
        self.sobremesas = [r for r in receitas if r.get("categoria", "").lower() == "sobremesa"]

    def selecionar_melhor_menu(self, tempo_max, custo_max, objetivo="lucro"):
    
        melhor_menu = None
        melhor_pontuacao = -float('inf') if objetivo in ["lucro", "avaliacao"] else float('inf')

        # fb
        for entrada in self.entradas:
            for principal in self.principais:
                for sobremesa in self.sobremesas:
                    
                    custo_total = entrada["custo_estimado"] + principal["custo_estimado"] + sobremesa["custo_estimado"]
                    tempo_total = entrada["tempo_preparo"] + principal["tempo_preparo"] + sobremesa["tempo_preparo"]
                    
                    # tira o qe viola
                    if custo_total > custo_max or tempo_total > tempo_max:
                        continue
                    lucro_total = entrada["lucro"] + principal["lucro"] + sobremesa["lucro"]
                    avaliacao_media = round((entrada["avaliacao"] + principal["avaliacao"] + sobremesa["avaliacao"]) / 3, 2)
                    valor_venda = custo_total + lucro_total

                    if objetivo == "lucro":
                        pontuacao_atual = lucro_total
                    elif objetivo == "avaliacao":
                        pontuacao_atual = avaliacao_media
                    elif objetivo == "tempo":
                        pontuacao_atual = tempo_total
                    else:
                        pontuacao_atual = lucro_total 

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
                            "dificuldade_logistica": "Média" 
                        }

        return melhor_menu