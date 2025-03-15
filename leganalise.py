import pandas as pd
import numpy as np
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from collections import Counter
import itertools
import matplotlib.pyplot as plt
import plotly.graph_objs as go

class analise:
    
    def __init__(self, data_base= 'BD_full_lotoFacil.xlsx', tamanho_amostra= 10):
        '''
        O objeto inicialmente criado é do tipo DataFrame do pandas.
        Como parâmetro é possível passar o data_base, que obrigatóriamente deve estar no formato ".xlsx"
        '''

        self.data_base = data_base

        self.dados = pd.read_excel(self.data_base, header= None)
        self.dados = self.dados.drop(0)
        #ordena os dados de forma ascendente utilizando a coluna [0] == concursos
        self.dados = self.dados.sort_values(by=0, ascending= False)
        self.tamanho_amostra = tamanho_amostra

    def coletar_dados(self):
        # Nome do arquivo onde os dados serão armazenados
        arquivo_excel = self.data_base

        # Verificar se o arquivo já existe
        if os.path.exists(arquivo_excel):
            # Carregar o arquivo existente
            df_existente = pd.read_excel(arquivo_excel)
            
            # Obter o último concurso registrado
            ultimo_concurso_registrado = df_existente['Concurso'].max()
            print(f"Último concurso registrado: {ultimo_concurso_registrado}")
        else:
            # Se o arquivo não existir, inicializar um DataFrame vazio
            df_existente = pd.DataFrame()
            ultimo_concurso_registrado = None

        # Configurar o ChromeDriver automaticamente com o webdriver_manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # URL da Lotofácil onde os sorteios estão listados
        url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx'
        driver.get(url)

        # Espera explícita para garantir que os elementos estejam carregados
        wait = WebDriverWait(driver, 15)

        # Inicializar lista para armazenar todos os números sorteados e outros detalhes
        todos_os_sorteios = []

        while True:
            try:
                # Localizar o elemento do concurso e data pelo XPath relativo
                concurso_elemento = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="ng-binding"]')))
                
                # Extrair o texto (ex: "Concurso 3205 (26/09/2024)")
                concurso_texto = concurso_elemento.text
                
                # Usar regex para capturar o número do concurso e a data
                concurso_numero = re.search(r'Concurso (\d+)', concurso_texto).group(1)
                concurso_data = re.search(r'\((\d{2}/\d{2}/\d{4})\)', concurso_texto).group(1)

                print(f"Número do Concurso: {concurso_numero}")
                print(f"Data do Concurso: {concurso_data}")
                
                # Verificar se o concurso já está registrado no arquivo existente
                if int(ultimo_concurso_registrado) and int(concurso_numero) <= int(ultimo_concurso_registrado):
                    print(f"Concurso {concurso_numero} já registrado. Finalizando a coleta.")
                    break
                
                # Espera até que os números sorteados estejam presentes na página
                elementos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.dezena')))
                
                if elementos:
                    # Extrair o texto (números sorteados) de cada elemento encontrado
                    numeros_pagina = [int(elemento.text) for elemento in elementos]
                    print(f"Números sorteados nesta página: {numeros_pagina}")
                    
                    # Adicionar o número do concurso, data e números sorteados à lista
                    todos_os_sorteios.append([int(concurso_numero), concurso_data] + numeros_pagina)
                
                else:
                    print("Nenhum número sorteado encontrado na página atual.")

                # Espera até que o elemento de carregamento desapareça
                wait.until(EC.invisibility_of_element((By.ID, "loading")))
                
                # Verifica se o botão "Anterior" está presente e clicável
                botao_anterior = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="carregarConcursoAnterior()"]')))
                
                if botao_anterior:
                    botao_anterior.click()
                    time.sleep(10)  # Aguarda a página carregar após o clique
                else:
                    print("Não há mais páginas anteriores.")
                    break
            
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                break

        # Organizar todos os sorteios novos em um DataFrame do Pandas
        colunas = ['Concurso', 'Data'] + [f'Número_{i+1}' for i in range(15)]
        df_novos_sorteios = pd.DataFrame(todos_os_sorteios, columns=colunas)

        # Exibir o DataFrame de novos sorteios (para ver o formato)
        # print(df_novos_sorteios)

        df_novos_sorteios['Concurso'] = df_novos_sorteios['Concurso'].astype(int)

        # converter os números para int
        for i in range(1, 16):
            df_novos_sorteios[f'Número_{i}'] = df_novos_sorteios[f'Número_{i}'].astype(int)

        # Se houver novos sorteios, salvar no arquivo XLSX
        if not df_novos_sorteios.empty:
            # Concatenar os novos sorteios com os existentes, se houver
            if not df_existente.empty:
                df_final = pd.concat([df_novos_sorteios, df_existente], ignore_index=True)
                self.dados = df_final
            else:
                df_final = df_novos_sorteios
                self.dados = df_final
            
            # Salvar no arquivo XLSX (sobrescreve o arquivo existente com os novos dados)
            df_final.to_excel(arquivo_excel, index=False, engine='openpyxl')
            print(f"Novos sorteios adicionados e salvos em {arquivo_excel}.")
        else:
            print("Nenhum sorteio novo foi coletado.")
        
        

        # Fechar o navegador ao final do processo
        driver.quit()
    
    # Função para calcular a frequência dos números em uma amostra
    def calcular_frequencia_amostra(self, tipo_amostra='news'):
        df = self.dados
        tamanho_amostra = self.tamanho_amostra
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
    
    def calc_pares_trincas_quadras(self):
        # Carregar o arquivo Excel
        dados = self.dados

        amostra = dados.head(self.tamanho_amostra).copy()

        # amostra = amostra.copy()

        # Juntar as colunas dos números sorteados (colunas 2 a 16, pois Python usa indexação a partir de 0)
        amostra['numeros_juntos'] = amostra.loc[:, 2:16].apply(lambda row: ','.join(row.astype(str)), axis=1)

        # Separar os números sorteados que estão agrupados em uma coluna
        amostra['numeros_juntos'] = amostra['numeros_juntos'].str.split(',')

        # Flatten todos os números sorteados em uma única lista
        todos_numeros = [list(map(int, sublist)) for sublist in amostra['numeros_juntos']]

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
        self.pares_df = pd.DataFrame(pares_counter.items(), columns=['Par', 'Frequência']).sort_values(by='Frequência', ascending=False, ignore_index= True)
        self.trincas_df = pd.DataFrame(trincas_counter.items(), columns=['Trinca', 'Frequência']).sort_values(by='Frequência', ascending=False, ignore_index= True)
        self.quadras_df = pd.DataFrame(quadras_counter.items(), columns=['Quadra', 'Frequência']).sort_values(by='Frequência', ascending=False, ignore_index= True)

        # # Salvar os resultados em arquivos Excel separados
        # pares_df.to_excel('frequencia_pares_lotofacil.xlsx', index=False)
        # trincas_df.to_excel('frequencia_trincas_lotofacil.xlsx', index=False)
        # quadras_df.to_excel('frequencia_quadras_lotofacil.xlsx', index=False)

        print("Cálculos realizados com sucesso!")

    def arredondar_customizado(self, valor):
        # Arredonda para baixo se for menor que 0.5 e para cima se for 0.5 ou maior
        return int(np.floor(valor + 0.5))

    def calcular_media_simples(self):
        df = self.dados
        num_sorteios = self.tamanho_amostra

        # Seleciona as colunas dos números sorteados (da terceira coluna em diante)
        numeros_sorteados = df.iloc[:, 2:]
        
        # Seleciona os dados retroativos (mais recentes) com base na quantidade de sorteios especificada
        dados_retroativos = numeros_sorteados.head(num_sorteios)
        
        # Calcula a média simples de cada coluna
        media_simples = dados_retroativos.mean()
        
        media_arredondada = media_simples.apply(self.arredondar_customizado)
        
        return media_arredondada
    
    def calcular_media_movel_simples(self, janela = 9):
        # Seleciona as colunas dos números sorteados (da terceira coluna em diante)
        numeros_sorteados = self.df.iloc[:, 2:]
        
        # Calcula a média móvel simples para cada coluna (número sorteado)
        media_movel = numeros_sorteados.rolling(window=janela).mean().apply(self.arredondar_customizado)
        
        return media_movel
    
    def plotar_barras_media_movel(self, coluna, janela):
        num_sorteios = self.tamanho_amostra
        # Seleciona os dados da coluna específica
        dados_coluna1 = self.dados.iloc[:num_sorteios, coluna]
        dados_coluna = dados_coluna1.iloc[::-1].reset_index(drop=True)

        # Calcula a média móvel simples
        media_movel = dados_coluna.rolling(window=janela).mean()

        # Remove valores NaN antes de aplicar o arredondamento
        media_movel_sem_nan = media_movel.dropna()

        # Aplica o arredondamento personalizado
        media_movel_arredondada = media_movel_sem_nan.apply(self.arredondar_customizado)

        self.media_movel_barras_arredondada = media_movel_arredondada

        # Configura o gráfico
        plt.figure(figsize=(12, 6))

        # Gráfico de barras para os números sorteados
        plt.bar(dados_coluna.index, dados_coluna, label='Sorteios', color='lightblue')

        # Linha para a média móvel simples
        plt.plot(media_movel_arredondada.index, media_movel_arredondada, label='Média Móvel Simples', color='orange', linewidth=2)

        # Títulos e legendas
        plt.title(f'Gráfico de Barras e Média Móvel - Coluna {coluna - 1} (Média móvel simples de {janela} períodos.)')
        plt.xlabel('Números Sorteados')
        plt.ylabel('Valores')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plotar_scatter_media_movel(self, coluna, janela):
        num_sorteios = self.tamanho_amostra

        # Seleciona os dados da coluna específica
        dados_coluna1 = self.dados.iloc[:num_sorteios, coluna]
        dados_coluna = dados_coluna1.iloc[::-1].reset_index(drop=True)

        # Calcula a média móvel simples
        media_movel = dados_coluna.rolling(window=janela).mean()

        # Calcular a média móvel exponêncial
        # media_movel = dados_coluna.ewm(span= janela, adjust=False).mean()

        # Remove valores NaN antes de aplicar o arredondamento
        media_movel_sem_nan = media_movel.dropna()

        # Aplica o arredondamento personalizado
        media_movel_arredondada = media_movel_sem_nan.apply(self.arredondar_customizado)

        self.media_movel_scatter_arredondada = media_movel_arredondada

        # Configura o gráfico
        plt.figure(figsize=(12, 6))

        # Gráfico de dispersão (scatter plot) para os números sorteados
        plt.scatter(dados_coluna.index, dados_coluna, label='Sorteios', color='blue', s=100)
        
        sorteado = 0
        
        # Verifica e marca os pontos vermelhos onde o sorteio foi igual à média móvel anterior
        for i in range(janela, len(dados_coluna)):
            if dados_coluna.iloc[i] == media_movel_arredondada.iloc[i - janela]:
                # Se o número sorteado for igual à média móvel do sorteio anterior, pinta de vermelho
                plt.scatter(i, dados_coluna.iloc[i], color='red', s=100, label='Sorteio = Média Móvel' if i == 1 else "")
                sorteado += 1

        # Linha para a média móvel simples
        plt.plot(media_movel_arredondada.index, media_movel_arredondada, label='Média Móvel Simples', color='orange', linewidth=2)

        # Colocar os números sorteados no eixo x
        plt.xticks(ticks=dados_coluna.index, labels="")

        # Força o eixo Y a mostrar apenas valores inteiros
        plt.yticks(np.arange(dados_coluna.min(), dados_coluna.max() + 1, 1))

        # Títulos e legendas
        plt.title(f'Gráfico de Pontos e Média Móvel - Coluna {coluna - 1} (Média móvel simples de {janela} períodos.)')
        plt.xlabel(f'Contagem números sorteados na média = {sorteado}\nRepresentando {float(sorteado/len(media_movel_arredondada)*100):.2f}% da amostra.')
        plt.ylabel('Valores')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plotar_scatter_media_movel_dash(self, coluna, janela):
        num_sorteios = self.tamanho_amostra
        # Seleciona os dados da coluna específica
        dados_coluna1 = self.dados.iloc[:num_sorteios, coluna]
        dados_coluna = dados_coluna1.iloc[::-1].reset_index(drop=True)

        # Converter a coluna para valores numéricos, ignorando erros
        dados_coluna = pd.to_numeric(dados_coluna, errors='coerce')

        # Calcula a média móvel simples e arredonda os valores para inteiros
        media_movel = dados_coluna.rolling(window=janela).mean().round(0)

        # Cria o gráfico com Plotly
        fig = go.Figure()

        # Adiciona os dados originais como pontos
        fig.add_trace(go.Scatter(
            x=list(range(len(dados_coluna))),
            y=dados_coluna,
            mode='markers',
            marker=dict(color='blue'),
            name='Dados Originais'
        ))

        # Adiciona a média móvel como linha
        fig.add_trace(go.Scatter(
            x=list(range(len(media_movel))),
            y=media_movel,
            mode='lines',
            name='Média Móvel'
        ))

        # Adiciona os pontos sorteados que estavam na média do sorteio passado
        for i in range(1, len(dados_coluna)):
            if dados_coluna[i] == media_movel[i-1]:
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[dados_coluna[i]],
                    mode='markers',
                    marker=dict(color='red', size=10),
                    name='Número Sorteado na Média'
                ))

        # Configurações adicionais do layout do gráfico
        fig.update_layout(
            title=f'Média Móvel Simples - Coluna {coluna}',
            xaxis_title='Índice',
            yaxis_title='Valor',
            legend_title='Legenda',
            yaxis=dict(tickformat="d"),  # Formato dos ticks do eixo y para mostrar apenas inteiros
            showlegend=False  # Remove a legenda do gráfico
        )

        return fig