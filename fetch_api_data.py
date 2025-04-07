import requests
import pandas as pd
import dask.dataframe as dd

# API URL for the top 100 cryptocurrencies

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page":"100",
    "page": 1,
    "sparkline":False
}

# Fetach data from API
response = requests.get(COINGECKO_URL, params=params)

if response.status_code == 200:
    data = response.json()

    # convert JSON to Pandas DataFrame
    df = pd.DataFrame(data)
    df.to_csv("cyptocurrency.csv")

    # convert Pnadas to dask DataFrame
    dask_df = dd.from_pandas(df, npartitions=2)
    
    # Display Dask dataFrame
    print(dask_df.head())

else:
    print("Error Fetching data:", response.status_code)