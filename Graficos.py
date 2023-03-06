#Importações
import pandas as pd
from pandas.core.frame import DataFrame
from dash import Dash, dcc, html, Input, Output
import plotly.express as px 

app = Dash(__name__, title = 'Criptomoedas')

#---------------------------------------------------------------------------------------------------------
#Grafico 1

#Ler .csv
df = pd.read_csv('coin_Bitcoin.csv')
df_array = df.values

#Gráfico de linha por dia
marketcap = []
dias = []

for linha in df_array:
    dias.append(linha[3])
    marketcap.append(linha[9])

fig1 = px.line(
    x=dias,
    y=marketcap,
)    

#Gráfico de linha por ano

#Filtro do eixo X
contador = 0
anos = []
while contador < 2991:
  dias[contador] = dias[contador].split('-')  
  anos.append(dias[contador][0])
  contador = contador+1

anos = sorted(set(anos))

#Filtro do eixo y
# O marketdic armazena os valores do marketcap diário referentes a cada ano

marketdic =	{
  '2013': [], # Ano/Key : valor(es) = (lista vazia)
  '2014': [],
  '2015': [],
  '2016': [],
  '2017': [],
  '2018': [],
  '2019': [],
  '2020': [],
  '2021': [],
}

cont = 0
while cont < 2991:
  for linha in df_array:
    for key in marketdic:
      if key == dias[cont][0]:
        marketdic[key].append(linha[9])
    cont = cont+1

def media(x):
  y = sum(marketdic[(x)])/len(marketdic[(x)])
  return y

marketcap_media = []
for key in marketdic:
  marketcap_media.append(media(key))

fig2 = px.line(
    x=anos,
    y=marketcap_media,
    title = 'Média anual do Marketcap do Bitcoin'
)

marketdic2 =	{
  '2013': [], 
  '2014': [],
  '2015': [],
  '2016': [],
  '2017': [],
  '2018': [],
  '2019': [],
  '2020': [],
  '2021': [],
}

c = 0
while c < 2991:
  for linha in df_array:
    for key in marketdic2:
      if key == dias[c][0]:
        marketdic2[key].append(linha[3])
    c = c+1

#---------------------------------------------------------------------------------------------------------
#Grafico 2

df = pd.read_csv('coin_Bitcoin.csv')
df1 = pd.read_csv('O_brabo.csv')

#transforma o Bitcoin.csv em lista
lista_bitcoin = df.values.tolist()

#transforma o Dolar.csv em lista
lista_dolar = df1.values.tolist()

#alocando os anos/open em uma nova lista (data_frame_dolar)

ano_dolar = []
price_dolar = []

for linha in lista_dolar:
  ano_dolar.append(linha[0])
  price_dolar.append(linha[1])
# change = 5 ; close = 1

# tratamento dos dados dolar ano


def hunter(ano_str):
  for x in range(0, len(ano_dolar) - 1):
    procura = ano_dolar[x].find(ano_str)
    if (procura >= 0):
      ano_dolar.pop(x)
    else:
      break


anos_fora_do_escopo = ["2001", "2002", "2003",
                       "2004", "2005", "2006",
                       "2007", "2008", "2009",
                       "2010", "2011", "2012"]
for y in range(100):
  for x in anos_fora_do_escopo:
      hunter(x)

#tratamento dos dados dolar price

numero_secreto = 142857


def hunter_price(numero):
 for x in range(0, 3084):
    if (price_dolar[0] != numero):
      price_dolar.pop(0)
    else:
      break


hunter_price(numero_secreto)

#alocando os anos/open em uma nova lista (data_frame_anos)
ano_bitcoin = []
price_bitcoin = []

for linha in lista_bitcoin:
  ano_bitcoin.append(linha[3])
  price_bitcoin.append(linha[7])
# open = 6 ; close = 7

# aumentano a escala para melhor visualização
constante_de_multiplicacao = 207
for x in range(len(price_dolar)):
  price_dolar[x] = price_dolar[x] * constante_de_multiplicacao

# GRÁFICO PRICE EM RELAÇÃO AO ANO (2013 A 2020)----DOLÁR

plot1 = px.line(x=ano_dolar, y=price_dolar, labels={
    y: "Price(USD$)",
    x: "Anos corridos"
}, color_discrete_sequence=px.colors.qualitative.T10, template='plotly_white')
#fig.update_xaxes(showticklabels=False)



plot2 = px.line(y=price_bitcoin, x=ano_bitcoin, title='Crypto moedas',
                color_discrete_sequence=px.colors.qualitative.T10, template='plotly_white')


#---------------------------------------------------------------------------------------------------------
#Grafico 3

df_1 = pd.read_csv('AllCoin.csv')
df_array_1 = df_1.values

anos1 = []
volume = []
name = []

for linha in df_array_1:
    anos1.append(linha[3])
    volume.append(linha[8])
    name.append(linha[1])

lista_volume = list(zip(anos1,volume, name))
avaliable_names = df_1['Name'].unique()

graph_volume= px.histogram(lista_volume, x=anos1, y=volume, color=name)

#---------------------------------------------------------------------------------------------------------
#Grafico 4

df_btc = pd.read_csv('coin_Bitcoin.csv')
df_btc_array = df_btc.values
df_eth = pd.read_csv('coin_Ethereum.csv')
df_eth_array = df_eth.values

marketcap_btc = []
marketcap_eth = []
data = []

for linha_btc in df_btc_array:
    for linha_eth in df_eth_array:
        if linha_btc[3] == linha_eth[3]:
            marketcap_btc.append(linha_btc[9])
            marketcap_eth.append(linha_eth[9])
            data.append(linha_btc[3])

# eixo Y
media_marketcap = []
df_marketcap = pd.DataFrame(zip(marketcap_btc, marketcap_eth, data), columns=['marketcap-btc', 'marketcap-eth', 'data'])
df_marketcap['year']= pd.DatetimeIndex(df_marketcap['data']).year
contador = 0
while contador < len(df_marketcap):
    media_marketcap = (df_marketcap['marketcap-btc'] + df_marketcap['marketcap-eth']/2)
    contador = contador + 1

min = df_marketcap['year'].min()
m = {str(year): str(year) for year in df_marketcap['year'].unique()}
graph_marketcap = px.line(x=df_marketcap['data'], y=media_marketcap)

#---------------------------------------------------------------------------------------------------------
#Grafico 5


df_moedas = pd.read_csv('https://raw.githubusercontent.com/Diaxiz/Python-UnB/main/Criptomoedas.csv')

media_preco = df_moedas.values.tolist()

Real, Libra, Euro, Kwanza, Yen = 5.16, 1.14, 1.00, 429.98, 143.36

valores = [Real, Libra, Euro, Kwanza, Yen]
valores_2 = ['Real', 'Libra', 'Euro', 'Kwanza', 'Yen']

#Criando lista vazia

valores_media = []

#Pegando as colunas, tirando a média e convertendo pra real

for coluna in media_preco:
  valores_media.append([((coluna[4]+coluna[5])/2)*Real,coluna[2],coluna[3]])

moedas = DataFrame(valores_media, columns=['Media Preco Dia','Moeda', 'Data'])

fig = px.line(moedas, x='Data', y='Media Preco Dia', color='Moeda')

#---------------------------------------------------------------------------------------------------------
#Layout do Dash

app.layout = html.Div(children=[
        html.H1(children='Criptomoedas',),
        html.Div(children=[  
          html.H3(children='Grupo B da turma 12')
        ]),
        html.Div(children=[
        html.H4(children='Marketcap do Bitcoin ao longo dos anos'),
          dcc.Dropdown(anos, value= None , id='anos')
        ]),
        html.Div(children=[
          dcc.Graph(
              id= 'Gráfico_Bitcoin',
              figure= fig1 
          )
        ]),
        html.Div(children=[
          html.H4(children='Comparação entre Bitcoin e dolár'),
          dcc.Dropdown(['Gráfico Dólar', 'Gráfico Bitcoin'], value='Gráfico Dólar', id='Moedas')
        ]),
        html.Div(children=[
            dcc.Graph(
                id='graph',
                figure= plot1
          )
        ]),
        html.Div(children=[
            html.H4(children='Volume de algumas criptomoedas'),
            dcc.Dropdown(
                id = 'dropdown',
                options=[{'label': i, 'value':i} for i in avaliable_names],value= None, multi = False, placeholder = 'Filtre as moedas'
          )
        ]),
        html.Div(children=[
          dcc.Graph(
            id = 'graph-volume'
          )
        ]),
        html.Div(children=[
            html.H4(children='Marketcap do Bitcoin e Ethereum'),
            dcc.Graph(
                id = 'graph-marketcap'
          )
        ]),
        html.Div(children=[
          dcc.Slider(
            id = "slider",
            min= df_marketcap['year'].min(),
            max = df_marketcap['year'].max(),
            value=df_marketcap['year'].min(),
            marks=m,
            step=None
          )
        ]),
        html.Div(children=[
            html.H4(children='Valor de algumas criptomoedas em diferentes cotações'),
            dcc.Dropdown(['Real', 'Libra', 'Euro', 'Kwanza', 'Yen'], value='Real', id='botao'),
        ]),
        html.Div(children=[
          dcc.Graph(
            id='grafico',
            figure=fig
          )
        ])
        
])

#---------------------------------------------------------------------------------------------------------
#Callbacks

@app.callback(
    Output('Gráfico_Bitcoin', 'figure'),
    Input('anos', 'value')
)
def atualizar_output(value):
    
    if value != None:
        for key in marketdic:
            if value == key:
                fig1 = px.line(
                    x = marketdic2[key],
                    y = marketdic[key],
                )
                
        return fig1
    else:
        return fig2


@app.callback(
    Output("graph", "figure"),
    Input("Moedas", "value")
)
def atualizar_output(value):  
    if value == 'Gráfico Dólar':
      return plot1
    elif value == 'Gráfico Bitcoin':
      return plot2


@app.callback(
    Output('graph-volume', 'figure'),
    Input('dropdown', 'value'))

def update_volume(value):
    ts = df_1[df_1["Name"].isin([value])]
    fig = px.histogram(ts, x="Date", y="Volume", color='Name' )
    if value == None:
        return graph_volume
    return fig


@app.callback(
    Output('graph-marketcap', 'figure'),
    Input('slider', 'value'))

def update_volume(selected_value):
    #ts = df_marketcap[df_marketcap["year"].isin([value])]
    filtered = df_marketcap[df_marketcap.year == selected_value]
    fig = px.line(filtered, x=df_marketcap['year'], y=media_marketcap)
    fig.update_layout(transition_duration=500)
    return fig



@app.callback(
    Output('grafico', 'figure'),
    Input('botao', 'value')
)
def update_output(value):
    if value == 'Real':

        valores_media = []

        #Pegando as colunas, tirando a média e convertendo pra real

        for coluna in media_preco:
            valores_media.append([((coluna[4]+coluna[5])/2)*Real,coluna[2],coluna[3]])

        moedas = DataFrame(valores_media, columns=['Media Preco Dia','Moeda', 'Data'])

        fig = px.line(moedas, x='Data', y='Media Preco Dia', color='Moeda')
    else:
        valores_media = []

        #Pegando as colunas, tirando a média e convertendo pra real

        for coluna in media_preco:
            valores_media.append([((coluna[4]+coluna[5])/2)*valores[valores_2.index(value)],coluna[2],coluna[3]])

        moedas = DataFrame(valores_media, columns=['Media Preco Dia','Moeda', 'Data'])

        fig = px.line(moedas, x='Data', y='Media Preco Dia', color='Moeda')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
