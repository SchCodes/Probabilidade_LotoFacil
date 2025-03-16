import pandas as pd
import numpy as np
import os
import re
import itertools
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import time
from collections import Counter
from typing import Dict, Tuple, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class AnaliseLotoFacil:
    
    def __init__(self, data_base: str = 'BD_full_lotoFacil.xlsx', tamanho_amostra: int = 10):
        """
        Classe para análise de dados da Lotofácil
        
        Parâmetros:
        data_base (str): Nome do arquivo de dados (formato .xlsx)
        tamanho_amostra (int): Tamanho padrão para amostras de análise
        """
        self.data_base = data_base
        self.tamanho_amostra = tamanho_amostra
        
        try:
            self.dados = self._carregar_dados()
            self._validar_estrutura_dados()
        except FileNotFoundError:
            self.dados = pd.DataFrame()

    def _carregar_dados(self) -> pd.DataFrame:
        """Carrega e prepara os dados do arquivo Excel"""
        df = pd.read_excel(self.data_base, header=None)
        df = df.drop(0).reset_index(drop=True)
        df = df.sort_values(by=0, ascending=False)
        return df

    def _validar_estrutura_dados(self) -> None:
        """Valida a estrutura básica do DataFrame"""
        if len(self.dados.columns) < 17:
            raise ValueError("O DataFrame não possui colunas suficientes")
        if not all(self.dados.iloc[:, 0].apply(lambda x: isinstance(x, (int, float)))):
            raise ValueError("Coluna de concurso inválida")

    def coletar_dados(self) -> None:
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

    def _obter_amostra(self) -> pd.DataFrame:
        """
        Retorna uma amostra dos dados com base no tamanho especificado.
        
        Retorna:
        pd.DataFrame: Amostra dos dados.
        """
        return self.dados.head(self.tamanho_amostra)

    def _calcular_max_sequencia(self) -> int:
        """
        Calcula o comprimento da maior sequência de números consecutivos em um mesmo sorteio.
        
        Retorna:
        int: Tamanho da maior sequência encontrada.
        """
        max_sequencia = 0
        amostra = self._obter_amostra()
        
        for _, row in amostra.iterrows():
            numeros = sorted(row.iloc[2:17])  # Ordena os números do sorteio
            sequencia_atual = 1
            maior_sequencia_sorteio = 1
            
            for i in range(1, len(numeros)):
                if numeros[i] == numeros[i-1] + 1:
                    sequencia_atual += 1
                    if sequencia_atual > maior_sequencia_sorteio:
                        maior_sequencia_sorteio = sequencia_atual
                else:
                    sequencia_atual = 1
            
            if maior_sequencia_sorteio > max_sequencia:
                max_sequencia = maior_sequencia_sorteio
        
        return max_sequencia
    
    def _calcular_distribuicao_pares(self) -> Dict[str, float]:
        """
        Calcula a distribuição de números pares e ímpares na amostra.
        
        Retorna:
        Dict[str, float]: Dicionário com a porcentagem de pares e ímpares.
        """
        amostra = self._obter_amostra()
        todos_numeros = amostra.iloc[:, 2:17].values.flatten().tolist()
        pares = sum(1 for num in todos_numeros if num % 2 == 0)
        impares = len(todos_numeros) - pares
        
        return {
            'pares': (pares / len(todos_numeros)) * 100,
            'impares': (impares / len(todos_numeros)) * 100
        }

    # ANÁLISE BÁSICA
    def calcular_estatisticas_basicas(self) -> Dict:
        """
        Retorna estatísticas descritivas básicas dos números sorteados na amostra.
        
        Retorna:
        Dict: Dicionário com diversas estatísticas
        """
        amostra = self._obter_amostra()
        numeros = amostra.iloc[:, 2:17].values.flatten().tolist()
        
        return {
            'numero_mais_frequente': Counter(numeros).most_common(1)[0][0],
            'numero_menos_frequente': Counter(numeros).most_common()[-1][0],            
            'maximo_sequencia': self._calcular_max_sequencia(),
            'distribuicao_pares': self._calcular_distribuicao_pares(),
            'media_soma': self.calcular_media_soma(),
            'media_repeticao': self._calcular_media_repeticao(),
            'frequencia_absoluta': dict(Counter(numeros)),
        }

    # ANÁLISE TEMPORAL
    def calcular_media_soma(self) -> float:
        """Calcula a média da soma dos números sorteados na amostra."""
        amostra = self._obter_amostra()
        return amostra.iloc[:, 2:17].sum(axis=1).mean()

    def calcular_frequencia_relativa(self, periodo: int = 10) -> pd.DataFrame:
        """
        Calcula a frequência relativa dos números por período na amostra.
        
        Parâmetros:
        periodo (int): Número de sorteios para agrupar
        
        Retorna:
        pd.DataFrame: DataFrame com frequências relativas por período
        """
        amostra = self._obter_amostra()
        grupos = [amostra[i:i+periodo] for i in range(0, len(amostra), periodo)]
        resultados = []

        for grupo in grupos:
            numeros = grupo.iloc[:, 2:17].values.flatten()
            freq = pd.Series(numeros).value_counts(normalize=True).to_dict()
            resultados.append(freq)

        return pd.DataFrame(resultados).fillna(0)
    
    def _calcular_media_repeticao(self) -> float:
        """
        Calcula a média de números repetidos entre sorteios consecutivos.
        
        Retorna:
        float: Média de repetição entre sorteios.
        """
        amostra = self._obter_amostra()
        repetidos = []
        
        for i in range(1, len(amostra)):
            numeros_anterior = set(amostra.iloc[i-1, 2:17]) # Números do sorteio anterior
            numeros_atual = set(amostra.iloc[i, 2:17]) # Números do sorteio atual
            repetidos.append(len(numeros_anterior.intersection (numeros_atual))) # Números repetidos
        
        return np.mean(repetidos)
    
    def calcular_intervalo_aparicoes(self) -> pd.DataFrame:
        """
        Calcula o intervalo médio entre aparições de cada número.
        Corrige problemas de valores negativos e NaN.
        
        Retorna:
        pd.DataFrame: DataFrame com números de 1 a 25 e estatísticas de intervalo
        """
        intervalos = {num: [] for num in range(1, 26)}
        ultima_posicao = {num: None for num in range(1, 26)}

        amostra = self._obter_amostra().sort_values(by=0, ascending=True)  # Ordenar por concurso CRESCENTE

        for idx, row in amostra.iterrows():
            concurso = row.iloc[0]  # Número do concurso (coluna 0)
            for num in row.iloc[2:17]:  # Colunas dos números sorteados
                if ultima_posicao[num] is not None:
                    intervalo = concurso - ultima_posicao[num]  # Intervalo baseado em concursos
                    intervalos[num].append(intervalo)
                ultima_posicao[num] = concurso  # Atualizar última posição pelo número do concurso

        # Calcular última aparição corretamente
        ultimo_concurso = amostra.iloc[-1, 0]  # Número do último concurso na amostra
        ultima_aparicao = {
            num: (ultimo_concurso - ultima_posicao[num] if ultima_posicao[num] is not None else np.nan)
            for num in range(1, 26)
        }

        # DataFrame final
        df = pd.DataFrame({
            'numero': range(1, 26),
            'media_intervalo': [np.mean(intervalos[num]) if intervalos[num] else np.nan for num in range(1, 26)],
            'max_intervalo': [max(intervalos[num]) if intervalos[num] else np.nan for num in range(1, 26)],
            'ultima_aparicao': [ultima_aparicao[num] for num in range(1, 26)]
        }).set_index('numero')

        return df

    # ANÁLISE COMBINATÓRIA
    def analisar_combinacoes(self, tamanho_grupo: int = 2) -> pd.DataFrame:
        """
        Analisa combinações de números de determinado tamanho na amostra.
        
        Parâmetros:
        tamanho_grupo (int): Tamanho das combinações a analisar (2-4)
        
        Retorna:
        pd.DataFrame: DataFrame com combinações e frequências
        """
        amostra = self._obter_amostra()
        combinacoes = []
        
        for _, row in amostra.iterrows():
            numeros = sorted(row.iloc[2:17])
            combinacoes.extend(itertools.combinations(numeros, tamanho_grupo))
            
        freq = Counter(combinacoes)
        df = pd.DataFrame.from_dict(freq, orient='index').reset_index()
        df.columns = ['Combinacao', 'Frequencia']
        return df.sort_values('Frequencia', ascending=False, ignore_index=True)

    # VISUALIZAÇÃO
    def plot_heatmap_frequencia(self):
        """
        Gera heatmap interativo das frequências numéricas na amostra.
        
        Retorna:
        go.Figure: Gráfico de heatmap interativo.
        """
        # Coletar dados de frequência
        freq = self.calcular_estatisticas_basicas()['frequencia_absoluta']
        
        # Filtrar apenas os números de 1 a 25
        nums = [num for num in range(1, 26)]  # Números de 1 a 25
        counts = [freq.get(num, 0) for num in nums]  # Frequências correspondentes

        # Criar o heatmap
        fig = go.Figure(data=go.Heatmap(
            z=[counts],  # Valores de frequência
            x=nums,      # Números (1 a 25)
            # Rótulo do eixo Y
            colorscale='Ice',  # Opções de paletas de cores: 'Cividis', 'Inferno', 'Magma', 'Plasma', 'Turbo', 'Jet', 'Hot', 'Cool', 'Rainbow'. Mais em: https://plotly.com/python/builtin-colorscales/
            colorbar=dict(title='Frequência'),
            hoverinfo='x+z',  # Mostrar número e frequência ao passar o mouse
        ))

        # Ajustar layout
        fig.update_layout(
            title='Mapa de Calor - Frequência dos Números (Lotofácil)',
            xaxis_title='Números',
            yaxis_title='',
            xaxis=dict(tickmode='linear', dtick=1, showgrid=False),  # Mostrar todos os números no eixo X
            yaxis=dict(showticklabels=False, showgrid=False),  # Ocultar rótulos do eixo Y
            height=400,  # Ajustar altura do gráfico
            width=800,   # Ajustar largura do gráfico
            margin=dict(l=50, r=50, b=50, t=50),  # Margens
            font=dict(size=14)  # Tamanho da fonte global
        )

        media_frequencia = np.mean(counts)

        # Adicionar anotações
        for i, num in enumerate(nums):
            fig.add_annotation(
                x=num, y=0,  # Posição da anotação
                text=str(counts[i]),  # Texto da anotação
                showarrow=False,  # Sem seta
                font=dict(
                    size=12, 
                    color='white' if counts[i] < media_frequencia else 'black' # Cor do texto
                    )  
            )

        return fig
    
    # UTILITÁRIOS
    def exportar_para_csv(self, arquivo: str = 'analise_lotofacil.csv') -> None:
        """Exporta dados básicos de análise para CSV"""
        estatisticas = self.calcular_estatisticas_basicas()
        pd.DataFrame.from_dict(estatisticas).to_csv(arquivo, index=False)

    def gerar_relatorio(self) -> str:
        """Gera um relatório textual resumido da análise"""
        estatisticas = self.calcular_estatisticas_basicas()
        relatorio = f"""
        RELATÓRIO DE ANÁLISE - LOTOFÁCIL
        ---------------------------------
        Período analisado: {self.tamanho_amostra} sorteios
        Número mais frequente: {estatisticas['numero_mais_frequente']}
        Número menos frequente: {estatisticas['numero_menos_frequente']}
        Média de repetição dos números entre sorteios: {estatisticas['media_repeticao']:.2f}
        Maior sequência encontrada: {estatisticas['maximo_sequencia']}
        Distribuição de pares e ímpares: {estatisticas['distribuicao_pares']['pares']:.2f}% pares, {estatisticas['distribuicao_pares']['impares']:.2f}% ímpares
        Média da soma dos números sorteados: {estatisticas['media_soma']:.2f}
        """
        return relatorio
    
    def sugerir_aposta(self, peso_frequencia=0.4, peso_intervalo=0.3, peso_combinacoes=0.3) -> List[int]:
        """
        Sugere números para apostas combinando múltiplas métricas estatísticas.
        
        Parâmetros:
        peso_frequencia (float): Peso para números mais frequentes (0-1)
        peso_intervalo (float): Peso para números atrasados (0-1)
        peso_combinacoes (float): Peso para combinações frequentes (0-1)
        
        Retorna:
        List[int]: 15 números sugeridos ordenados
        """
        # Coletar dados
        estatisticas = self.calcular_estatisticas_basicas()
        intervalos = self.calcular_intervalo_aparicoes()
        pares = self.analisar_combinacoes(tamanho_grupo=2)
        trincas = self.analisar_combinacoes(tamanho_grupo=3)
        max_seq = estatisticas['maximo_sequencia']

        # 1. Score por frequência, intervalo e última aparição
        scores = {}
        for num in range(1, 26):
            # Frequência normalizada
            score_freq = estatisticas['frequencia_absoluta'].get(num, 0) / self.tamanho_amostra
            
            # Intervalo (tratar NaN)
            media_intervalo = intervalos.loc[num, 'media_intervalo']
            if pd.isna(media_intervalo):
                score_intervalo = 0  # Números que apareceram apenas uma vez ou nunca
            else:
                score_intervalo = 1 / (media_intervalo + 1e-6)  # Evitar divisão por zero
            
            # Última aparição (quanto maior, mais "atrasado" o número está)
            ultima_aparicao = intervalos.loc[num, 'ultima_aparicao']
            if pd.isna(ultima_aparicao):
                score_atraso = 0  # Números que nunca apareceram
            else:
                score_atraso = ultima_aparicao / self.tamanho_amostra  # Normalizar
            
            # Score total
            scores[num] = (
                (peso_frequencia * score_freq) +
                (peso_intervalo * score_intervalo) +
                (peso_intervalo * score_atraso)  # Adicionar peso para números atrasados
            )

        # 2. Adicionar peso de combinações
        for row in pd.concat([pares, trincas]).head(10).itertuples(index=False):
            combo = row.Combinacao  # Acessa a coluna 'Combinacao'
            freq = row.Frequencia   # Acessa a coluna 'Frequencia'
            for num in combo:
                scores[num] += peso_combinacoes * freq

        # 3. Seleção balanceada
        top_numeros = sorted(scores, key=lambda x: scores[x], reverse=True)[:20]

        # 4. Balancear pares/ímpares
        distribuicao = estatisticas['distribuicao_pares']
        num_pares = int(15 * (distribuicao['pares'] / 100))
        num_impares = 15 - num_pares

        # 5. Evitar sequências longas
        candidatos = self._evitar_sequencias(top_numeros, max_seq)

        # 6. Seleção final
        pares = [n for n in candidatos if n % 2 == 0][:num_pares]
        impares = [n for n in candidatos if n % 2 != 0][:num_impares]
        selecao = pares + impares

        # Completar se necessário
        if len(selecao) < 15:
            selecao += [n for n in top_numeros if n not in selecao][:15-len(selecao)]

        return sorted(selecao[:15])

    def _evitar_sequencias(self, numeros, max_seq):
        """Filtra números para evitar sequências longas"""
        numeros_ordenados = sorted(numeros)
        sequencias = []
        
        # Identificar sequências
        seq_atual = [numeros_ordenados[0]]
        for num in numeros_ordenados[1:]:
            if num == seq_atual[-1] + 1:
                seq_atual.append(num)
            else:
                sequencias.append(seq_atual)
                seq_atual = [num]
        sequencias.append(seq_atual)
        
        # Remover sequências longas
        filtrados = []
        for seq in sequencias:
            if len(seq) > max_seq:
                filtrados.extend(seq[:max_seq])
            else:
                filtrados.extend(seq)
        
        return filtrados