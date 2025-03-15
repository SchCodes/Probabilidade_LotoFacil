# Probabilidade LotoFacil

## Descrição
O **Leganálise** é um projeto desenvolvido para coletar, analisar e visualizar dados relacionados aos sorteios da LotoFácil, uma das loterias mais populares do Brasil. O objetivo deste projeto é a realização de estudos para entender melhor as probabilidades e padrões nos resultados da loteria.

## Funcionalidades
- Coleta de dados de sorteios da LotoFácil.
- Análise de frequência de números sorteados.
- Cálculos estatísticos, incluindo médias e distribuições.
- Visualização de dados com gráficos de barras e scatter plots.

## Tecnologias Utilizadas
- Python
- Pandas
- Selenium
- Matplotlib
- Plotly
- Jupyter Notebook (para análise interativa)

## Bibliotecas Necessárias

Este projeto utiliza as seguintes bibliotecas Python:

- **os**: Para interações com o sistema operacional. **(biblioteca padrão do python)**
- **pandas**: Para manipulação e análise de dados.
- **selenium**: Para automação de navegadores web e coleta de dados.
- **webdriver_manager.chrome**: Para gerenciar o ChromeDriver e garantir a compatibilidade com a versão do Chrome.
- **time**: Para pausas entre ações na automação. **(biblioteca padrão do python)**
- **re**: Para manipulação de expressões regulares. **(biblioteca padrão do python)**
- **collections.Counter**: Para contar a frequência de itens. **(biblioteca padrão do python)**
- **itertools**: Para criar iteradores eficientes para loops. **(biblioteca padrão do python)**
- **matplotlib.pyplot**: Para criação de gráficos.
- **plotly.graph_objs**: Para criação de gráficos interativos.

### Instalação das Bibliotecas

Você pode instalar todas as bibliotecas necessárias usando o `pip`. Execute o seguinte comando no seu terminal:

```bash
pip install pandas selenium webdriver-manager matplotlib plotly openpyxl
```

## Uso

### Inicialização

Para iniciar a análise, você deve criar uma instância da classe `analise`:

```python
import leganalise as leg

lotofacil = leg.analise(tamanho_amostra=21) # instancia a classe analise
```

### Funções Disponíveis

#### `coletar_dados()`
Coleta os dados dos sorteios da LotoFácil diretamente do site da Caixa e salva em um arquivo Excel.

#### `calcular_frequencia_amostra(tipo_amostra='news')`
Calcula a frequência dos números sorteados em uma amostra. Os tipos de amostra podem ser:
- `'random'`: Seleciona uma amostra aleatória.
- `'old'`: Seleciona os sorteios mais antigos.
- `'news'`: Seleciona os sorteios mais recentes.

#### `calc_pares_trincas_quadras()`
Calcula a frequência de pares, trincas e quadras de números sorteados.

#### `arredondar_customizado(valor)`
Arredonda um valor para o inteiro mais próximo.

#### `calcular_media_simples()`
Calcula a média simples dos números sorteados.

#### `calcular_media_movel_simples(janela=9)`
Calcula a média móvel simples dos números sorteados com uma janela especificada.

#### `plotar_barras_media_movel(coluna, janela)`
Plota um gráfico de barras com a média móvel simples para uma coluna específica e uma janela especificada.

#### `plotar_scatter_media_movel(coluna, janela)`
Plota um gráfico de dispersão (scatter plot) com a média móvel simples para uma coluna específica e uma janela especificada.

#### `plotar_scatter_media_movel_dash(coluna, janela)`
Plota um gráfico de dispersão interativo com Plotly, mostrando a média móvel simples para uma coluna específica e uma janela especificada.

## Exemplo de Uso

```python
import leganalise as leg

# Instanciar a classe analise
lotofacil = leg.analise(tamanho_amostra=21)

# Coletar dados
lotofacil.coletar_dados()

# Calcular frequência dos números sorteados
frequencia = lotofacil.calcular_frequencia_amostra()

# Calcular pares, trincas e quadras
lotofacil.calc_pares_trincas_quadras()

# Plotar gráficos
lotofacil.plotar_barras_media_movel(coluna=2, janela=5)
lotofacil.plotar_scatter_media_movel(coluna=2, janela=5)
fig = lotofacil.plotar_scatter_media_movel_dash(coluna=2, janela=5)
fig.show()
```

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Para isso, faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.