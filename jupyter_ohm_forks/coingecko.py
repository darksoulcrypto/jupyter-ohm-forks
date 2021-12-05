import requests
import pandas as pd

def add_coingecko_data(df):
    session = requests.session()
    session.headers = {
            "Accept": "application/json"
        }

    uri = "https://api.coingecko.com"
    coins = '%2C'.join(df['Name'])
    path = f"api/v3/coins/markets?vs_currency=usd&ids={coins}"

    data = session.get(f"{uri}/{path}").json()

    return pd.merge(df, pd.DataFrame(data), left_on='Ticker', right_on='symbol') # TODO - figure how to merge this shit