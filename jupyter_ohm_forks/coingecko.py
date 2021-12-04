import requests

def add_cg_data(df):
    session = requests.session()
    session.headers = {
            "Accept": "application/json"
        }

    session.uri = "https://api.coingecko.com"
    path = "/api/v3/coins/markets?vs_currency=usd"
    

    return df