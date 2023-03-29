import requests
import os
from twilio.rest import Client

############################# STOCKS GETTER #############################
EMPRESA = 'microsoft'
STOCK = "MSFT"
API_KEY_STOCKS = 'MHQUYP5W2JBFWY7I'
ENDPOINT_STOCKS = 'https://www.alphavantage.co/query'
API_KEY_NEWS = '7536a63cb0924832887fee383e81d506'
ENDPOINT_NEWS = 'https://newsapi.org/v2/everything'


parametros_stocks = {
    'function' : 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol' : STOCK,
    'outputsize':'compact',
    'apikey' : API_KEY_STOCKS,
}

parametros_news = {
    'q': EMPRESA,
    'from': '2023-02-20',
    'sortBy': 'popularity',
    'apiKey': API_KEY_NEWS
}

peticion = requests.get(ENDPOINT_STOCKS, params = parametros_stocks).json()
peticion_news = requests.get(ENDPOINT_NEWS, params=parametros_news).json()

# Convierto el json a una lista para obtener los dos primeros valores (los dos ultimos dias habiles)
lista_dias = list(peticion['Time Series (Daily)'].items())
fecha_hoy = lista_dias[0][0]
fecha_ayer = lista_dias[1][0]

stock_hoy = peticion['Time Series (Daily)'][fecha_hoy]
stock_ayer = peticion['Time Series (Daily)'][fecha_ayer]
close_price_hoy = stock_hoy['4. close']
close_price_ayer = stock_ayer['4. close']

print(f"{STOCK} al {fecha_hoy}:{stock_hoy}")
print(f"{STOCK} al {fecha_ayer}:{stock_ayer}")

# Chequeo si el close_price de hoy fue menor o mayor al close_price de ayer
diferencia = float(close_price_hoy) - float(close_price_ayer)

def get_diff():
    if diferencia>0:
        print(f"+${diferencia}")
        return f"+${diferencia}"
    elif diferencia<0:
        print(f"${diferencia}")
        return f"${diferencia}"
    else:
        print(f"${diferencia}")
        return f'$={diferencia}'


################################## NEWS GETTER ##################################
lista = peticion_news['articles']
titulares = [noticia['title'] for noticia in lista[:3]]
noticias = [noticia['description'] for noticia in lista[:3]]


################################## SMS ##################################
account_sid = "YOUR_APIKEY_HERE"
auth_token = 'YOUR_TOKEN_HERE'
client = Client(account_sid, auth_token)
message = client.messages.create(
      body=f"{STOCK}:{get_diff()}.\n{titulares[0]}.\n {noticias[0]}.\n{titulares[1]}."
           f"\n{noticias[1]}.\n{titulares[2]}.\n{noticias[2]}.",
      from_="YOUR_TWILLIO_NUMBER",
      to="YOUR_CELLPHONE_NUMBER"
)
