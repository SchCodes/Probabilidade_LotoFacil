import pandas as pd
from collections import Counter

#carregar a planilha com os sorteios
dados = pd.read_excel('data_lotofacil_full.xlsx')

#separar os números sorteados agrupados em uma coluna
dados[0] = dados[0].str.split(',')

todos_numeros = dados.values.flatten()

frequencia = Counter(todos_numeros)

frequencia_df = pd.DataFrame(list(frequencia.items()), columns=['Número', 'Frequência'])
