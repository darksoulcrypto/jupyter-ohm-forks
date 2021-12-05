import pandas as pd
from jupyter_ohm_forks.coingecko import add_coingecko_data


def test_coingecko():
    req_columns = [
        "Name",
        "Ticker",
        "id",
        "symbol",
        "name",
        "image",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "fully_diluted_valuation",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_24h",
        "price_change_percentage_24h",
        "market_cap_change_24h",
        "market_cap_change_percentage_24h",
        "circulating_supply",
        "total_supply",
        "max_supply",
        "ath",
        "ath_change_percentage",
        "ath_date",
        "atl",
        "atl_change_percentage",
        "atl_date",
        "roi",
        "last_updated",
    ]

    df1 = pd.read_csv("forks.csv")
    df2 = add_coingecko_data(df1)
    assert list(df2.columns) == req_columns
    assert len(df1) == len(df2)