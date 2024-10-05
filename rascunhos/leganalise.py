class analise:
    
    def __init__(self, data_base= 'BD_full_lotoFacil.xlsx'):

        '''
        O objeto inicialmente criado é do tipo DataFrame do pandas.
        Como parâmetro é possível passar o data_base, que obrigatóriamente deve estar no formato ".xlsx"
        '''
    
        from pandas import read_excel as pd_re

        self.data_base = data_base

        self.dados = pd_re(self.data_base, header= None)
        self.dados = self.dados.drop(0)
        self.dados = self.dados.sort_values(by=0, ascending= False)
    
    # Função para calcular a frequência dos números em uma amostra
    def calcular_frequencia_amostra(self, tamanho_amostra, tipo_amostra='news'):

        df = self.dados
        self.tamanho_amostra = tamanho_amostra
        self.tipo_amostra = tipo_amostra
    
        if tipo_amostra == 'random':
            # Selecionar uma amostra aleatória. 
            # Obs: random state fixo! Para amostras totalmente aleatórias, excluir este parâmetro.
            # amostra = df.sample(n=tamanho_amostra, random_state=42)
            amostra = df.sample(n=tamanho_amostra)
        elif tipo_amostra == 'old':
            # Selecionar os n antigos sorteios
            amostra = df.tail(tamanho_amostra)
        elif tipo_amostra == 'news':
            # Selecionar os n recentes sorteios
            amostra = df.head(tamanho_amostra)
        else:
            raise ValueError("Tipo de amostra inválido. Use 'aleatoria', 'old' ou 'news'.")

        # Calcular a frequência dos números sorteados na amostra
        frequencias = {}
        for _, row in amostra.iterrows():
            # Pegar os números sorteados (colunas Num1 até Num15)
            numeros_sorteio = row.iloc[2:17].values
            for numero in numeros_sorteio:
                if numero in frequencias:
                    frequencias[numero] += 1
                else:
                    frequencias[numero] = 1
        
        # Ordenar as frequências
        frequencias_ordenadas = dict(sorted(frequencias.items(), key=lambda x: x[1], reverse=True))
        
        return frequencias_ordenadas
    
