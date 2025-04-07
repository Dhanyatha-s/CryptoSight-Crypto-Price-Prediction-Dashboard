import streamlit as st
import pandas as pd
import seaborn as sns
import squarify
import numpy as np
import matplotlib.pyplot as plt
from connection import engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# --- Fetch Data ---
@st.cache_data
def fetch_data():
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT symbol, name, current_price, market_cap, total_volume, 
                   high_24h, low_24h, price_change_percentage_24h, 
                   ath, ath_change_percentage 
            FROM crypto_market_data;
        """, conn)
    return df

df = fetch_data()

# --- Calculate KPIs ---
df["volatility"] = df["high_24h"] - df["low_24h"]  # Market Volatility
df["market_dominance"] = (df["market_cap"] / df["market_cap"].sum()) * 100
df["liquidity_ratio"] = df["total_volume"] / df["market_cap"]
df["ath_gap_percentage"] = df["ath_change_percentage"].abs()
df["price_ma7"] = df["current_price"].rolling(window=7).mean()

# Define features and target
X = df[["current_price", "total_volume", "high_24h", "low_24h", "price_change_percentage_24h"]]
y = df["market_cap"]

# Preprocess the data (standardize it, if needed)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Assuming model is a pre-trained RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_scaled, y)  # Train the model if it's not pre-trained

# --- Prediction with the Model ---
df["predicted_market_cap"] = model.predict(X_scaled)

# --- Sidebar Filters ---
st.sidebar.header("📊 Filter Data")
top_n = st.sidebar.slider("Select Top N Cryptos:", 5, 20, 10)
metric = st.sidebar.selectbox("Choose Metric:", ["Market Cap", "Price Change % (24h)", "Liquidity Ratio"])
refresh = st.sidebar.button("🔄 Refresh Data")

# --- Prediction Selectbox ---
symbols = df["symbol"].tolist()  # List of symbols from the data
prediction_symbol = st.sidebar.selectbox("Predict with Symbol:", symbols)



# --- Display Prediction for Selected Symbol ---
selected_symbol_data = df[df["symbol"] == prediction_symbol]
predicted_market_cap = selected_symbol_data["predicted_market_cap"].values[0]

# Display the selected symbol and its predicted market cap in the sidebar
st.sidebar.subheader(f"Prediction for {prediction_symbol}")
st.sidebar.write(f"Predicted Market Cap: ${predicted_market_cap:,.2f}")

if refresh:
    st.rerun()

# Handle NaN Values
df["volatility"] = (df["high_24h"] - df["low_24h"]).fillna(0)
df["ath_gap_percentage"] = df["ath_change_percentage"].abs().fillna(0)

# --- Title & Summary ---
st.title("CryptoSight")
st.markdown("Real-time cryptocurrency market analytics with insights into volatility, liquidity, and dominance.")

# --- Display Key Metrics ---

st.markdown(
    """
    <style>
        .metric-box {
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #444;  /* Darker border */
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            background-color: #222;  /* Dark background */
            color: #fff;  /* White text for contrast */
        }
        .up {color: #28a745; font-size: 24px;}  /* Green for positive */
        .down {color: #dc3545; font-size: 24px;}  /* Red for negative */
        .metric-box span {
            font-size: 24px;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


# Market Cap
col1.markdown(
    f'<div class="metric-box">📈 Market Cap (Total)<br><span style="font-size:24px;">${df["market_cap"].sum() / 1_000_000:,.1f}M</span></div>',
    unsafe_allow_html=True
)


# Volatility
volatility_trend = "up" if df["volatility"].mean() > 0 else "down"
col2.markdown(
    f'<div class="metric-box">⚡ Avg Volatility<br><span class="{volatility_trend}">${df["volatility"].mean():,.2f}</span></div>', 
    unsafe_allow_html=True
)

# ATH Drop
ath_trend = "down" if df["ath_gap_percentage"].mean() > 0 else "up"
col3.markdown(
    f'<div class="metric-box">📉 Avg ATH Drop<br><span class="{ath_trend}">{df["ath_gap_percentage"].mean():.2f}%</span></div>', 
    unsafe_allow_html=True
)


# --- 📊 Market Dominance (Treemap) ---
st.subheader("📊 Market Dominance of Top Cryptos")
top_dominant = df.nlargest(top_n, "market_dominance")
fig, ax = plt.subplots(figsize=(12, 6))
squarify.plot(
    sizes=top_dominant["market_dominance"],
    label=top_dominant["symbol"],
    alpha=0.8,
    color=sns.color_palette("coolwarm", top_n)
)
plt.axis("off")
st.pyplot(fig)

# --- 📈 Price Trend with Moving Average ---
st.subheader("📈 Crypto Price Trend with 7-Day Moving Average")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=df.index, y=df["current_price"], label="Current Price", color="blue", ax=ax)
sns.lineplot(x=df.index, y=df["price_ma7"], label="7-Day Moving Avg", color="red", ax=ax)
plt.legend()
st.pyplot(fig)


# --- 📉 ATH Drop (Top Losers) ---
st.subheader("📉 Top Cryptos with Highest Drop from ATH")
top_drops = df.nlargest(top_n, "ath_gap_percentage")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="ath_gap_percentage",
    y="symbol",
    palette="magma",
    data=top_drops,
    ax=ax
)
plt.xlabel("Drop from All-Time High (%)")
st.pyplot(fig)

# --- 📊 Top 10 Performing Cryptos ---
# --- 📊 Top Performing Cryptos in Last 24 Hours ---
st.subheader("📊 Top Performing Cryptos in Last 24 Hours")
top_performers = df.nlargest(top_n, "price_change_percentage_24h")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="price_change_percentage_24h",
    y="symbol",
    hue="symbol",  # Assigning hue to 'symbol'
    palette="coolwarm",
    data=top_performers
)
plt.legend(title="Cryptos", loc="lower right")  # Add legend back if necessary
st.pyplot(fig)


# --- Footer ---
st.markdown("---")
st.markdown("🚀 **Built with Streamlit & Matplotlib** |  Data powered by Snowflake Database") 

