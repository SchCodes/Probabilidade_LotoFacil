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

# Nome do arquivo onde os dados serão armazenados
arquivo_excel = 'BD_full_lotoFacil.xlsx'

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
        if ultimo_concurso_registrado and int(concurso_numero) <= int(ultimo_concurso_registrado):
            print(f"Concurso {concurso_numero} já registrado. Finalizando a coleta.")
            break
        
        # Espera até que os números sorteados estejam presentes na página
        elementos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.dezena')))
        
        if elementos:
            # Extrair o texto (números sorteados) de cada elemento encontrado
            numeros_pagina = [elemento.text for elemento in elementos]
            print(f"Números sorteados nesta página: {numeros_pagina}")
            
            # Adicionar o número do concurso, data e números sorteados à lista
            todos_os_sorteios.append([concurso_numero, concurso_data] + numeros_pagina)
        
        else:
            print("Nenhum número sorteado encontrado na página atual.")

        # Espera até que o elemento de carregamento desapareça
        wait.until(EC.invisibility_of_element((By.ID, "loading")))
        
        # Verifica se o botão "Anterior" está presente e clicável
        botao_anterior = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="carregarConcursoAnterior()"]')))
        
        if botao_anterior:
            botao_anterior.click()
            time.sleep(5)  # Aguarda a página carregar após o clique
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
print(df_novos_sorteios)

# Se houver novos sorteios, salvar no arquivo XLSX
if not df_novos_sorteios.empty:
    # Concatenar os novos sorteios com os existentes, se houver
    if not df_existente.empty:
        df_final = pd.concat([df_novos_sorteios, df_existente], ignore_index=True)
    else:
        df_final = df_novos_sorteios
    
    # Salvar no arquivo XLSX (sobrescreve o arquivo existente com os novos dados)
    df_final.to_excel(arquivo_excel, index=False, engine='openpyxl')
    print(f"Novos sorteios adicionados e salvos em {arquivo_excel}.")
else:
    print("Nenhum sorteio novo foi coletado.")

# Fechar o navegador ao final do processo
driver.quit()
