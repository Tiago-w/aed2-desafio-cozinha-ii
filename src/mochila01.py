class MenuVIPOtimizador:
    def __init__(self, receitas):
        self.receitas = receitas

    def otimizar_por_tempo(self, tempo_maximo, criterio_maximizacao='avaliacao'):
        """
        Resolve o Problema da Mochila 0/1 usando Programação Dinâmica.
        Maximiza o critério escolhido respeitando o tempo máximo.
        """
        n = len(self.receitas)
        
        # Criação da matriz de Programação Dinâmica: dp[item][tempo]
        # Preenchida com zeros inicialmente
        dp = [[0.0] * (tempo_maximo + 1) for _ in range(n + 1)]

        # Preenchendo a matriz
        for i in range(1, n + 1):
            receita = self.receitas[i - 1]
            tempo_receita = int(receita.get('tempo_preparo', 0))
            
            # Se o JSON não tiver o campo, simulamos um valor para não quebrar
            valor_receita = float(receita.get(criterio_maximizacao, 5.0))

            for t in range(1, tempo_maximo + 1):
                if tempo_receita <= t:
                    # Escolha: Levar esta receita ou não levar? O que dá maior valor?
                    dp[i][t] = max(
                        dp[i - 1][t], 
                        dp[i - 1][t - tempo_receita] + valor_receita
                    )
                else:
                    # Não cabe no tempo, herda o valor de cima
                    dp[i][t] = dp[i - 1][t]

        # Recuperando quais receitas foram escolhidas (Backtracking na matriz)
        menu_escolhido = []
        t_restante = tempo_maximo
        
        for i in range(n, 0, -1):
            # Se o valor mudou em relação à linha de cima, significa que o item foi incluído
            if dp[i][t_restante] != dp[i - 1][t_restante]:
                receita_escolhida = self.receitas[i - 1]
                menu_escolhido.append(receita_escolhida)
                t_restante -= int(receita_escolhida.get('tempo_preparo', 0))

        # Reverte para ficar na ordem natural
        menu_escolhido.reverse()
        
        valor_total = dp[n][tempo_maximo]
        tempo_gasto = tempo_maximo - t_restante
        
        return menu_escolhido, valor_total, tempo_gasto