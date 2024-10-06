# Probabilidade LotoFacil

## Descrição
O **Leganálise** é um projeto desenvolvido para coletar, analisar e visualizar dados relacionados aos sorteios da LotoFácil, uma das loterias mais populares do Brasil. O objetivo deste projeto é a realização de estudos para entender melhor as probabilidades e padrões nos resultados da loteria.

## Funcionalidades
- Coleta de dados de sorteios da LotoFácil.
- Análise de frequência de números sorteados.
- Cálculos estatísticos, incluindo médias e distribuições.

## Tecnologias Utilizadas
- Python
- Pandas
- Selenium
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

### Instalação das Bibliotecas

Você pode instalar todas as bibliotecas necessárias usando o `pip`. Execute o seguinte comando no seu terminal:

```bash
pip install pandas selenium webdriver-manager
```

# Probabilidade de Acertar 15 Números na Lotofácil

A Lotofácil é uma das loterias mais populares no Brasil, onde o jogador deve escolher **15 números entre 25** e aguardar o sorteio dos 15 números vencedores. Este documento descreve como calcular as chances de acertar todos os 15 números utilizando o conceito de **combinação**.

### Fórmula para Combinação

Usamos a seguinte fórmula de combinação para calcular as probabilidades:

![Fórmula de Combinação](https://latex.codecogs.com/png.latex?C(n,%20k)%20=%20\frac{n!}{k!%20\cdot%20(n%20-%20k)!})

Onde:
- `n` é o número total de números disponíveis (no caso, 25),
- `k` é o número de números escolhidos (no caso, 15).

### Cálculo Passo a Passo

1. **Total de combinações possíveis (escolher 15 números de 25):**

![Total de Combinações](https://latex.codecogs.com/png.latex?C(25,%2015)%20=%20\frac{25!}{15!%20\cdot%20(25%20-%2015)!})

Resultado:

![Resultado Combinações](https://latex.codecogs.com/png.latex?C(25,%2015)%20=%203.268.760)

2. **Combinações favoráveis para acertar todos os 15 números:**

Para acertar exatamente os 15 números sorteados, você deve:
   - Acertar todos os 15 números escolhidos,
   - Não errar nenhum dos 10 números restantes.

Ou seja:

![Combinações Favoráveis](https://latex.codecogs.com/png.latex?C(15,%2015)%20=%201)

![Combinações Não Escolhidas](https://latex.codecogs.com/png.latex?C(10,%200)%20=%201)

3. **Probabilidade de acertar os 15 números:**

A probabilidade de acertar é a razão entre as combinações favoráveis e o total de combinações possíveis:

![Probabilidade](https://latex.codecogs.com/png.latex?P%20=%20\frac{1}{C(25,%2015)}%20=%20\frac{1}{3.268.760}%20\approx%200,0000306)

Ou seja, a chance de acertar os 15 números em uma aposta de 15 números na Lotofácil é de **1 em 3.268.760**, ou aproximadamente **0,0000306** (0,00003%).

### Conclusão

As chances de acertar todos os 15 números na Lotofácil são muito pequenas, mas é sempre bom lembrar que na loteria, a diversão está em participar! Boa sorte, e que sua persistência traga grandes conquistas!
