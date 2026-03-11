import streamlit as st
from google.cloud import bigquery
import plotly.graph_objects as go
import pandas as pd
import os
from google.oauth2 import service_account

st.set_page_config(
    page_title="FinTrack DaaS",
    page_icon="📈",
    layout="wide"
)

st.title("📈 FinTrack DaaS — Financial Market Signals")
st.markdown("Real-time alerts for volume anomalies and moving average signals across IBEX 35, Nasdaq, ETFs and Crypto.")

@st.cache_resource
def get_client():
    if os.path.exists("gcloud-key.json"):
        return bigquery.Client.from_service_account_json("gcloud-key.json")
    else:
        credentials_dict = st.secrets["gcloud_key"]
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        return bigquery.Client(credentials=credentials, project="fintrack-daas")

@st.cache_data
def load_tickers():
    client = get_client()
    query = """
        SELECT DISTINCT ticker
        FROM `fintrack-daas.raw.mart_stock_signals`
        ORDER BY ticker
    """
    df = client.query(query).to_dataframe(create_bqstorage_client=False)
    return df["ticker"].tolist()

@st.cache_data
def load_ticker_data(ticker):
    client = get_client()
    query = f"""
        SELECT *
        FROM `fintrack-daas.raw.mart_stock_signals`
        WHERE ticker = '{ticker}'
        ORDER BY price_date ASC
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

# Sidebar
st.sidebar.header("Filters")
tickers = load_tickers()
selected_ticker = st.sidebar.selectbox("Select a ticker", tickers)

# Cargar datos
df = load_ticker_data(selected_ticker)

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Signal", df["cross_signal"].iloc[-1])

with col2:
    last_close = df["close_price"].iloc[-1]
    st.metric("Last Close Price", f"{last_close:.2f}")

with col3:
    volume_alerts = df["flag_volume_alert"].sum()
    st.metric("Volume Alerts (2y)", int(volume_alerts))

# Gráfico de precios y medias móviles
st.subheader(f"Price & Moving Averages — {selected_ticker}")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["price_date"],
    y=df["close_price"],
    name="Close Price",
    line=dict(color="#1f77b4", width=1)
))

fig.add_trace(go.Scatter(
    x=df["price_date"],
    y=df["sma_50"],
    name="SMA 50",
    line=dict(color="#ff7f0e", width=1.5)
))

fig.add_trace(go.Scatter(
    x=df["price_date"],
    y=df["sma_200"],
    name="SMA 200",
    line=dict(color="#2ca02c", width=1.5)
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, width='stretch')

# Tabla de alertas de volumen
st.subheader("📋 Volume Anomaly Alerts")

alerts = df[df["flag_volume_alert"] == True][
    ["price_date", "ticker", "close_price", "volume", "avg_volume_10d"]
].sort_values("price_date", ascending=False)

if len(alerts) > 0:
    st.dataframe(alerts, width='stretch')
else:
    st.info("No volume alerts found for this ticker.")