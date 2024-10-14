import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import leganalise as leg

# Inicializar a aplicação Dash
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Função para gerar os gráficos
def gerar_grafico(m, janela):
    analise = leg.analise(tamanho_amostra=21)  # Usar a instância existente de 'analise'
    fig = analise.plotar_scatter_media_movel_dash(m, janela)
    return fig

# Função para gerar 15 gráficos
def gerar_15_graficos(janela):
    graficos = []
    for i in range(2, 17):
        fig = gerar_grafico(i, janela)
        graficos.append(dcc.Graph(figure=fig, id=f'graph-{i}'))
    return graficos

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Gráficos Lotofácil"),
    # dcc.Dropdown(
    #     id='dropdown',
    #     options=[{'label': f'n={i}', 'value': i} for i in range(2, 16)],
    #     value=1
    # ),
    html.Div(
        gerar_15_graficos(5),  # Gera os 15 gráficos com janela = 3
        style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '20px'}
    )
])

# Callback para atualizar o gráfico com base na seleção do dropdown
@app.callback(
    Output('graph-1', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_n):
    fig = gerar_grafico(selected_n, 5)  # Inclua o valor de 'janela' aqui
    return fig

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)