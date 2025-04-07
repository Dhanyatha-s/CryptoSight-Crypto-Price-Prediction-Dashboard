from connection import engine, snowflake_url
import pandas as pd
import dask.dataframe as dd


# define sql query
query = "SELECT * FROM crypto_market_data;"

# Fetch data using Pandas
def fetch_with_pandas():
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Fetch data using Dask :--- processing
def fetch_with_dask():
    pandas_df = fetch_with_pandas()  # Get Pandas DataFrame first
    df_dask = dd.from_pandas(pandas_df, npartitions=2)  # Convert to Dask
    return df_dask

if __name__ == "__main__":
    # Fetch & display first 5 rows from pandas df
    pandas_df = fetch_with_pandas()
    print("Data fetched with pandas")
    print(pandas_df.head(2))

    # Fetch & display first 5 rows from pandas df
    try:
        dask_df = fetch_with_dask()
        print("\n✅ Data fetched with Dask (Lazy Loading):")
        print(dask_df.head(2))  # Compute Dask DataFrame
    except Exception as e:
        print("\n❌ Dask failed to fetch data:", e)

