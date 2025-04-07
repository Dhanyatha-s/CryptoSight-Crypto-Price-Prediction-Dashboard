import dask.dataframe as dd
import pandas as pd
import requests
from connection import engine

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": "100",
    "page": 1,
    "sparkline": False
}

# Fetch data from API
response = requests.get(COINGECKO_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully from API!")
else:
    print("Failed to fetch data from API!")
    exit()

# Convert JSON to Pandas DataFrame
df = pd.DataFrame(data)

# Convert Pandas to Dask DataFrame
dask_df = dd.from_pandas(df, npartitions=2)

# Convert Dask DataFrame back to Pandas before inserting
df_pandas = dask_df.compute()

# Insert into Snowflake (REMOVE `USE DATABASE`)
df_pandas.to_sql("crypto_market_data", con=engine, if_exists="replace", index=False)

print("Data successfully inserted into Snowflake")
