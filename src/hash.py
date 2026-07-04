class TabelaHash:
    def __init__(self, tamanho_inicial=100):
        self.tamanho = tamanho_inicial
        self.tabela = [[] for _ in range(self.tamanho)]

    def _calcular_hash(self, conteudo_texto):
        soma = sum(ord(char) for char in conteudo_texto)
        indice = soma % self.tamanho
        return soma, indice

    def gerar_assinatura(self, nome, ingredientes):
        ingredientes_str = "".join(sorted(ingredientes)).lower()
        conteudo = f"{nome.lower()}{ingredientes_str}"
        return self._calcular_hash(conteudo)

    def inserir(self, id_receita, nome, ingredientes):
        assinatura_forte, indice = self.gerar_assinatura(nome, ingredientes)
        self.tabela[indice].append((id_receita, nome, assinatura_forte))

    def verificar_integridade(self, id_receita, nome, ingredientes_atuais):
        assinatura_atual_forte, indice = self.gerar_assinatura(nome, ingredientes_atuais)
        
        for tupla in self.tabela[indice]:
            id_salvo, nome_salvo, assinatura_salva_forte = tupla
            if id_salvo == id_receita:
                return assinatura_salva_forte == assinatura_atual_forte
        return False

    def auditoria_de_duplicados_e_conflitos(self):
        mapa_assinaturas = {}  
        mapa_nomes = {}       
        for balde in self.tabela:
            for id_rec, nome_rec, ass_forte in balde:
                if ass_forte not in mapa_assinaturas:
                    mapa_assinaturas[ass_forte] = []
                mapa_assinaturas[ass_forte].append((id_rec, nome_rec))

                nome_norm = nome_rec.lower().strip()
                if nome_norm not in mapa_nomes:
                    mapa_nomes[nome_norm] = []
                mapa_nomes[nome_norm].append((id_rec, ass_forte))

        duplicados = {ass: lista for ass, lista in mapa_assinaturas.items() if len(lista) > 1}

        conflitos = {}
        for nome_norm, registros in mapa_nomes.items():
            if len(registros) > 1:
                todas_assinaturas = {item[1] for item in registros}
                if len(todas_assinaturas) > 1:
                    conflitos[nome_norm] = registros

        return duplicados, conflitos