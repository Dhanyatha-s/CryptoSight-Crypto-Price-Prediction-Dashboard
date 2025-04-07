from connection import engine
import pandas as pd
from data_transformation import process_data


# save transformed data to snowflake
def save_to_snowflake():
    transformed_df = process_data().compute()

    with engine.connect() as conn:
        transformed_df.to_sql(
            "crypto_market_cleaned",
            con = conn,
            if_exists = "replace",
            index = False
        )
print("✅ Transformed data saved to Snowflake!")

if __name__ == "__main__":
    save_to_snowflake()