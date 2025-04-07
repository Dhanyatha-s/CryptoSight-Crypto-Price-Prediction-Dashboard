from sqlalchemy import Table, Column, Integer, String, Float,MetaData
from connection import engine

# Define table Schema
metadata = MetaData()
crypto_table = Table(
    "crypto_market_data", metadata,
    Column("id", String, primary_key=True),
    Column("symbol", String),
    Column("name", String),
    Column("image", String),
    Column("current_price", Float),
    Column("market_cap", Float),
    Column("market_cap_rank", Integer),
    Column("fully_diluted_valuation", Float),
    Column("total_volume", Float),
    Column("high_24h", Float),
    Column("low_24h", Float),
    Column("price_change_24h", Float),
    Column("price_change_percentage_24h", Float),
    Column("market_cap_change_24h", Float),
    Column("market_cap_change_percentage_24h", Float),
    Column("circulating_supply", Float),
    Column("total_supply", Float),
    Column("max_supply", Float),
    Column("ath", Float),
    Column("ath_change_percentage", Float),
    Column("ath_date", String),
    Column("atl", Float),
    Column("atl_change_percentage", Float),
    Column("atl_date", String),
    Column("roi", String),
    Column("last_updated", String)
)

metadata.create_all(engine)
print("Table 'crypto_market_data' created successfully!")


