# Análise Lotofácil

Este projeto tem como objetivo realizar análises estatísticas dos resultados da Lotofácil. Através de técnicas de web scraping utilizando Selenium, o script coleta os dados dos sorteios no site oficial das Loterias Caixa e executa diversos cálculos e visualizações para identificar padrões e tendências nos números sorteados.

## Funcionalidades

- **Coleta de Dados**:  
  Realiza web scraping no site oficial da Lotofácil para obter os resultados dos sorteios e armazena os dados em um arquivo Excel (`BD_full_lotoFacil.xlsx`).

- **Análise Estatística**:  
  Calcula estatísticas descritivas, como:
  - Número mais e menos frequente;
  - Média de repetições entre sorteios;
  - Comprimento da maior sequência de números consecutivos;
  - Média da soma dos números sorteados;
  - Distribuição de números pares e ímpares.

- **Análise Combinatória**:  
  Analisa combinações de números (pares, trincas, etc.) para identificar padrões na frequência das combinações.

- **Visualização Interativa**:  
  Gera um heatmap interativo utilizando Plotly para visualizar a frequência dos números sorteados.

- **Sugestão de Apostas**:  
  Sugere 15 números para apostas combinando múltiplas métricas estatísticas (frequência, intervalo de aparição, combinações) e balanceando a distribuição de pares e ímpares.

## Requisitos

- **Python**: Versão 3.7 ou superior.
- **Bibliotecas Python**:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `plotly`
  - `openpyxl`
  - `selenium`
  - `webdriver_manager`
  - Outras bibliotecas padrão: `os`, `re`, `itertools`, `collections`, `time`, `typing`

Você pode instalar as dependências utilizando o `pip`:

```bash
pip install pandas numpy matplotlib plotly openpyxl selenium webdriver_manager
```

Infelizmente, não posso abrir uma tela de edição em tempo real aqui, mas posso te ajudar de outra forma. Vou fornecer o conteúdo completo do arquivo Markdown (`.md`) em um formato que você pode copiar e colar diretamente em um arquivo `.md` no seu computador. Dessa forma, você pode salvar o arquivo e abri-lo em um editor de texto ou Markdown.

Aqui está o conteúdo completo:

---
---
---
# Como Usar a Classe "AnaliseLotoFacil"

Aqui está um guia simples e didático para usar as principais funções da classe `AnaliseLotoFacil`.

---

## 1. **Iniciar a Análise**
Para começar, você precisa criar uma instância da classe `AnaliseLotoFacil`. Isso é feito da seguinte forma:

```python
analise = AnaliseLotoFacil(data_base='BD_full_lotoFacil.xlsx', tamanho_amostra=10)
```

- **`data_base`**: O nome do arquivo Excel onde os dados dos sorteios estão armazenados. Se não for passado, o padrão é `'BD_full_lotoFacil.xlsx'`.
- **`tamanho_amostra`**: Quantos sorteios recentes você quer analisar. O padrão é 10.

---

## 2. **Coletar Dados**
Se você ainda não tem os dados dos sorteios, pode coletá-los diretamente do site da Lotofácil:

```python
analise.coletar_dados()
```

- Essa função faz uma busca automática no site da Lotofácil e salva os resultados no arquivo Excel especificado.

---

## 3. **Ver Estatísticas Básicas**
Para ver informações como o número mais frequente, o menos frequente, a média da soma dos números e outras métricas:

```python
estatisticas = analise.calcular_estatisticas_basicas()
print(estatisticas)
```

- **O que você obtém**:
  - Número mais frequente.
  - Número menos frequente.
  - Maior sequência de números consecutivos.
  - Distribuição de pares e ímpares.
  - Média da soma dos números sorteados.
  - Frequência de cada número.

---

## 4. **Calcular a Média da Soma**
Se você quer saber a média da soma dos números sorteados em cada concurso:

```python
media_soma = analise.calcular_media_soma()
print(f"Média da soma dos números: {media_soma}")
```

---

## 5. **Ver Frequência Relativa**
Para entender como os números se comportam em períodos específicos (por exemplo, a cada 10 sorteios):

```python
frequencia_relativa = analise.calcular_frequencia_relativa(periodo=10)
print(frequencia_relativa)
```

- **O que você obtém**: A frequência com que cada número apareceu no período escolhido.

---

## 6. **Calcular Intervalos de Aparição**
Para saber quanto tempo, em média, um número leva para aparecer novamente:

```python
intervalos = analise.calcular_intervalo_aparicoes()
print(intervalos)
```

- **O que você obtém**:
  - Intervalo médio entre aparições de cada número.
  - Maior intervalo registrado.
  - Última aparição de cada número.

---

## 7. **Analisar Combinações**
Se você quer saber quais pares ou trincas de números aparecem juntos com mais frequência:

```python
combinacoes = analise.analisar_combinacoes(tamanho_grupo=2)  # Para pares
print(combinacoes)
```

- **`tamanho_grupo`**: Pode ser 2 (pares), 3 (trincas) ou 4 (quadras).

---

## 8. **Gerar um Heatmap**
Para visualizar a frequência dos números em um gráfico colorido e interativo:

```python
fig = analise.plot_heatmap_frequencia()
fig.show()
```

- **O que você vê**: Um mapa de calor onde as cores representam a frequência dos números.

---

## 9. **Exportar Dados para CSV**
Se você quer salvar as estatísticas em um arquivo CSV para análise posterior:

```python
analise.exportar_para_csv(arquivo='analise_lotofacil.csv')
```

- **`arquivo`**: Nome do arquivo CSV onde os dados serão salvos.

---

## 10. **Gerar um Relatório**
Para obter um resumo textual da análise:

```python
relatorio = analise.gerar_relatorio()
print(relatorio)
```

- **O que você obtém**: Um texto organizado com as principais métricas e conclusões.

---

## 11. **Sugerir Números para Aposta**
Se você quer uma sugestão de números para apostar, baseada em análise estatística:

```python
aposta_sugerida = analise.sugerir_aposta(peso_frequencia=0.5, peso_intervalo=0.3, peso_combinacoes=0.2)
print(f"Números sugeridos: {aposta_sugerida}")
```

- **`peso_frequencia`**: Peso para números que aparecem com mais frequência.
- **`peso_intervalo`**: Peso para números que estão "atrasados" (há muito tempo não aparecem).
- **`peso_combinacoes`**: Peso para números que costumam aparecer juntos.

---

## Resumo

| Função                        | O Que Faz                                                                 |
|-------------------------------|---------------------------------------------------------------------------|
| `__init__`                    | Inicia a análise com um arquivo de dados e tamanho da amostra.            |
| `coletar_dados`               | Coleta dados dos sorteios diretamente do site da Lotofácil.               |
| `calcular_estatisticas_basicas` | Retorna estatísticas como números mais frequentes, média da soma, etc.    |
| `calcular_media_soma`         | Calcula a média da soma dos números sorteados.                            |
| `calcular_frequencia_relativa` | Mostra a frequência dos números em períodos específicos.                  |
| `calcular_intervalo_aparicoes` | Calcula o intervalo médio entre aparições de cada número.                 |
| `analisar_combinacoes`        | Analisa quais números costumam aparecer juntos.                           |
| `plot_heatmap_frequencia`     | Gera um gráfico de calor interativo das frequências.                      |
| `exportar_para_csv`           | Salva as estatísticas em um arquivo CSV.                                  |
| `gerar_relatorio`             | Gera um relatório textual com as principais métricas.                     |
| `sugerir_aposta`              | Sugere números para apostar com base em análise estatística.              |

---
Agora você está pronto para usar a classe `AnaliseLotoFacil`!
---