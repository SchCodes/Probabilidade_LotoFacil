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

# Cálculo das Probabilidades de Acertar 15 Números na Lotofácil

Este repositório tem como objetivo explicar e calcular as probabilidades de acertar **15 números entre 25**, apostando **15 números**, no jogo da Lotofácil, utilizando o conceito de **combinação**.

Na Lotofácil, 15 números são sorteados de um conjunto de 25 disponíveis, e a aposta também consiste em 15 números. A fórmula para calcular as combinações possíveis é:

\[
C(n, k) = \frac{n!}{k! \cdot (n - k)!}
\]

Onde:
- \( n \) é o total de números disponíveis (25),
- \( k \) é o número de números a serem sorteados ou apostados (15).

## Passo a Passo

### 1. Total de combinações possíveis
Precisamos calcular o número de combinações possíveis ao escolher **15 números de 25**. A fórmula da combinação nos dá:

\[
C(25, 15) = \frac{25!}{15! \cdot (25 - 15)!} = \frac{25!}{15! \cdot 10!}
\]

Após realizar o cálculo, obtemos:

\[
C(25, 15) = 3.268.760
\]

### 2. Combinações Favoráveis
Para acertar todos os **15 números sorteados**, você precisa escolher corretamente os 15 números:

\[
C(15, 15) = 1
\]

Além disso, os 10 números restantes que não foram sorteados não devem ser escolhidos:

\[
C(10, 0) = 1
\]

Portanto, a quantidade de combinações favoráveis é **1**, já que é necessário acertar todos os 15 números e não escolher nenhum dos 10 restantes.

### 3. Probabilidade de Acertar
A probabilidade de acertar os 15 números em uma aposta é dada pela razão entre as combinações favoráveis e o total de combinações possíveis:

\[
P = \frac{1}{C(25, 15)}
\]

Substituindo o valor calculado de \( C(25, 15) \):

\[
P = \frac{1}{3.268.760} \approx 0,0000306
\]

Ou seja, a probabilidade de acertar os 15 números em uma aposta de 15 números na Lotofácil é de **1 em 3.268.760**, o que corresponde a aproximadamente **0,00003%** ou **0,0000306 de probabilidade**.

## Conclusão
A chance de acertar todos os 15 números em uma única aposta é extremamente pequena. Este exemplo ilustra como a matemática das combinações pode ser usada para entender as probabilidades de jogos de loteria.

---
