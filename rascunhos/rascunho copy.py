import pandas as pd
from collections import Counter

#carregar a planilha com os sorteios
dados = pd.read_excel('BD_full_lotoFacil.xlsx', header= None)
print(f'{dados.head(10)}\n')

# Juntar as colunas dos números sorteados (colunas 2 a 16, pois Python usa indexação a partir de 0)
dados['numeros_juntos'] = dados.loc[:, 2:16].apply(lambda row: ','.join(row.astype(str)), axis=1)
dados['numeros_juntos']

#separar os números sorteados agrupados em uma coluna
dados['numeros_juntos'] = dados['numeros_juntos'].str.split(',')
dados = dados.drop(0)

todos_numeros = [int(num) for sublist in dados['numeros_juntos'] for num in sublist]

frequencia = Counter(todos_numeros)

frequencia_df = pd.DataFrame(list(frequencia.items()), columns=['Número', 'Frequência'])

frequencia_df = frequencia_df.sort_values(by='Frequência', ascending= False)

frequencia_df.to_csv('frequencia_full.csv', index=False)
frequencia_df.to_excel('frequencia_full.xlsx', index=False)