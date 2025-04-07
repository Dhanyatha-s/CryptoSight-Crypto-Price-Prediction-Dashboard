# %% [markdown]
# # AI-Powered ETL Pipeline with API Deployment

# %% [markdown]
# ## Transformation of data

# %%
import sys 
import os 
import pandas as pd 
import dask.dataframe as dd

# %%
# Adding modules 
import os
import sys
project_paths = os.path.abspath("D:\databricks project\database project 2")

if project_paths not in sys.path:
    sys.path.append(project_paths)

import fetch_api_data
import connection
import Create_table
import insert_data
import fetch_data


# %%
# fetch data 
from connection import engine

def fetch_data():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM crypto_market_data;", conn)
    return df

df = fetch_data()
df


# %%
# Gather the Info
df.info()

# %%
# check for missing value
df.isnull().sum()

# %%
def process_data():
    df = fetch_data()
    ddf = dd.from_pandas(df,npartitions=4)

    # Drop columns with too many missing values
    cols_to_drop = ["image", "roi"]
    ddf = ddf.drop(columns=cols_to_drop, errors="ignore")

    # Drop the columns
    col_to_drop = ["image","roi"]
    ddf = ddf.drop(columns=col_to_drop, errors="ignore")

    # Fill the missing Values
    ddf= ddf.fillna( {"max_supply": 0})

    # Convert columns to appropriate types
    ddf["market_cap_rank"] = ddf["market_cap_rank"].astype("int32")
    ddf["circulating_supply"] = ddf["circulating_supply"].astype("float32")

    # Convert datetime columns
    ddf["last_updated"] = dd.to_datetime(ddf["last_updated"])

    print("Data transformation completed!")

    return ddf

if __name__ == "__main__":
    transformed_data = process_data()
    print("Transformed data preview:")
    print(transformed_data.head())
    
