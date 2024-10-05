import pandas as pd
from collections import Counter
import itertools

# Carregar o arquivo Excel
dados = pd.read_excel('BD_full_lotoFacil.xlsx', header= None)

# Eliminar a linha de índice indesejada
dados = dados.drop(0)

# Juntar as colunas dos números sorteados (colunas 2 a 16, pois Python usa indexação a partir de 0)
dados['numeros_juntos'] = dados.loc[:, 2:16].apply(lambda row: ','.join(row.astype(str)), axis=1)

# Separar os números sorteados que estão agrupados em uma coluna
dados['numeros_juntos'] = dados['numeros_juntos'].str.split(',')

# Flatten todos os números sorteados em uma única lista
todos_numeros = [list(map(int, sublist)) for sublist in dados['numeros_juntos']]

# Contar pares e trincas
pares_counter = Counter()
trincas_counter = Counter()
quadras_counter = Counter()

for sorteio in todos_numeros:
    # Obter todos os pares
    pares = list(itertools.combinations(sorteio, 2))
    pares_counter.update(pares)
    
    # Obter todas as trincas
    trincas = list(itertools.combinations(sorteio, 3))
    trincas_counter.update(trincas)

    # Obter todas as quadras
    quadras = list(itertools.combinations(sorteio, 4))
    quadras_counter.update(quadras)

# Criar DataFrames para pares e trincas
pares_df = pd.DataFrame(pares_counter.items(), columns=['Par', 'Frequência']).sort_values(by='Frequência', ascending=False)
trincas_df = pd.DataFrame(trincas_counter.items(), columns=['Trinca', 'Frequência']).sort_values(by='Frequência', ascending=False)
quadras_df = pd.DataFrame(quadras_counter.items(), columns=['Quadra', 'Frequência']).sort_values(by='Frequência', ascending=False)

# Exibir os DataFrames
print("Frequência de Pares:")
print(pares_df.head(10))  # Exibir os 10 pares mais frequentes
print("\nFrequência de Trincas:")
print(trincas_df.head(10))  # Exibir as 10 trincas mais frequentes
print("\nFrequência de Quadras:")
print(quadras_df.head(10))  # Exibir as 10 quadras mais frequentes

# Salvar os resultados em arquivos Excel separados
pares_df.to_excel('frequencia_pares_lotofacil.xlsx', index=False)
trincas_df.to_excel('frequencia_trincas_lotofacil.xlsx', index=False)
quadras_df.to_excel('frequencia_quadras_lotofacil.xlsx', index=False)

print("Resultados salvos com sucesso nos arquivos 'frequencia_pares_lotofacil.xlsx', 'frequencia_trincas_lotofacil.xlsx' e 'frequencia_quadras_lotofacil.xlsx'")
