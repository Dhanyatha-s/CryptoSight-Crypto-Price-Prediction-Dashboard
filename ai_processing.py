from connection import engine
import pandas as pd
import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def fetch_cleaned_data():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM crypto_market_cleaned;", conn)
    return df

# Predicting Future Price Change
def ai_processing():
    df = fetch_cleaned_data()
    print("fetched cleaned data")

    # convert to dask dataframe
    ddf = dd.from_pandas(df, npartitions=4)

    # Select Features & Target
    features = ["market_cap", "total_volume", "circulating_supply"]
    target = "price_change_percentage_24h"

    # split data 
    x_train, y_train, x_test, y_test = train_test_split(ddf[features],ddf[target], test_size = 0.2,random_state=42)

    # Convert to Pandas for Training
    X_train, X_test, y_train, y_test = X_train.compute(), X_test.compute(), y_train.compute(), y_test.compute()

    