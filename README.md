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

Para calcular as chances de acertar **15 números entre 25** apostando **15 números** na Lotofácil, você pode usar o conceito de **combinação**.

Na Lotofácil, 15 números são sorteados entre os 25 disponíveis, e a aposta também consiste em 15 números. A fórmula para calcular as combinações possíveis é:

\[
C(n, k) = \frac{n!}{k! \cdot (n - k)!}
\]

Onde:
- \( n \) é o total de números disponíveis (25),
- \( k \) é o número de números a serem sorteados ou apostados (15).

Agora, você precisa calcular o número de combinações possíveis para o sorteio e também para as combinações favoráveis.

### Passo a passo:

1. **Total de combinações possíveis** (escolher 15 números de 25):

\[
C(25, 15) = \frac{25!}{15! \cdot (25 - 15)!} = \frac{25!}{15! \cdot 10!}
\]

2. **Combinando 15 números corretos** (se você acertar todos):

\[
C(15, 15) = 1 \quad \text{(você precisa acertar todos os 15 números que escolheu)}
\]

3. **Combinando os 10 números restantes que não foram sorteados** (escolher 0 dos 10 que faltam):

\[
C(10, 0) = 1
\]

Portanto, a quantidade de combinações favoráveis é 1 (já que você precisa acertar todos os 15 números e não pode errar nenhum dos 10 restantes).

4. **Probabilidade de acertar**:

A probabilidade de acertar os 15 números em uma aposta é dada pela razão entre as combinações favoráveis e o total de combinações possíveis:

\[
P = \frac{1}{C(25, 15)}
\]

Calculando \( C(25, 15) \):

\[
C(25, 15) = 3.268.760
\]

Assim, a probabilidade de acertar os 15 números é:

\[
P = \frac{1}{3.268.760} \approx 0,0000306
\]

Ou seja, a chance de acertar os 15 números em uma aposta de 15 números na Lotofácil é de **1 em 3.268.760**, aproximadamente 0,00003%, ou 0,0000306 de probabilidade.

Essa é uma chance extremamente pequena, como ocorre em muitos jogos de loteria.