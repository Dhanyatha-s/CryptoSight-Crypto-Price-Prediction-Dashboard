import pandas as pd
import seaborn as sns
import squarify
import numpy as np
import matplotlib.pyplot as plt
from connection import engine

def fetch_data():
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT symbol, name, current_price, market_cap, total_volume, 
                   high_24h, low_24h, price_change_percentage_24h, 
                   ath, ath_change_percentage 
            FROM crypto_market_data;
        """, conn)
    return df

# Fetch data
df = fetch_data()

# ✅ Calculate KPIs
df["volatility"] = df["high_24h"] - df["low_24h"]  # Market Volatility
df["market_dominance"] = (df["market_cap"] / df["market_cap"].sum()) * 100  # Market Dominance
df["liquidity_ratio"] = df["total_volume"] / df["market_cap"]  # Liquidity Analysis
df["ath_gap_percentage"] = df["ath_change_percentage"].abs()  # ATH Drop %
df["price_ma7"] = df["current_price"].rolling(window=7).mean()  # 7-day Moving Average

# ✅ Top performers
top_performers = df.nlargest(10, "price_change_percentage_24h")
top_dominant = df.nlargest(10, "market_dominance")
top_drops = df.nlargest(15, "ath_gap_percentage")

# 🎨 Set Seaborn Theme
sns.set(style="whitegrid")

# 📊 Market Volatility Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["volatility"], bins=30, kde=True, color="steelblue")
plt.title("Market Volatility Distribution")
plt.xlabel("Volatility")
plt.ylabel("Frequency")
plt.show()

# 📊 Market Dominance (Treemap)
plt.figure(figsize=(12, 6))
squarify.plot(
    sizes=top_dominant["market_dominance"],
    label=top_dominant["symbol"],
    alpha=0.8,
    color=sns.color_palette("coolwarm", 10)
)
plt.title("Market Dominance of Top Cryptos")
plt.axis("off")
plt.show()

# 📊 Top 10 Performing Cryptos (Fixed Seaborn Warning)
plt.figure(figsize=(12, 6))
sns.barplot(
    x="price_change_percentage_24h",
    y="symbol",
    hue="symbol",
    palette="coolwarm",
    legend=False,
    data=top_performers
)
plt.xlabel("Price Change % (24h)")
plt.ylabel("Crypto Symbol")
plt.title("Top 10 Performing Cryptos in Last 24 Hours")
plt.show()

# 📊 Liquidity Analysis (Scatter Plot)
plt.figure(figsize=(12, 6))
sns.scatterplot(
    x=df["market_cap"],
    y=df["liquidity_ratio"],
    hue=df["symbol"],
    size=df["total_volume"],
    sizes=(20, 500),
    palette="viridis"
)
plt.xscale("log")
plt.xlabel("Market Cap (Log Scale)")
plt.ylabel("Liquidity Ratio")
plt.title("Liquidity Analysis of Cryptos")
plt.legend(title="Symbol", bbox_to_anchor=(1, 1))
plt.show()

# 📊 ATH Price Drop (Fixed Seaborn Warning)
plt.figure(figsize=(12, 6))
sns.barplot(
    x="ath_gap_percentage",
    y="symbol",
    hue="symbol",
    palette="magma",
    legend=False,
    data=top_drops
)
plt.xlabel("Drop from All-Time High (%)")
plt.ylabel("Crypto Symbol")
plt.title("Top 15 Cryptos with Highest Drop from ATH")
plt.show()

# 📈 Moving Average for Market Trend
plt.figure(figsize=(12, 6))
sns.lineplot(x=df.index, y=df["current_price"], label="Current Price", color="blue")
sns.lineplot(x=df.index, y=df["price_ma7"], label="7-Day Moving Avg", color="red")
plt.title("Crypto Price Trend with 7-Day Moving Average")
plt.legend()
plt.show()
