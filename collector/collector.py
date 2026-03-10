import yfinance as yf
import pandas as pd
from datetime import datetime, timezone

TICKERS = [
    # IBEX 35
    "SAN.MC", "BBVA.MC", "ITX.MC", "IBE.MC", "REP.MC",
    "TEF.MC", "AMS.MC", "FER.MC", "ANA.MC", "ELE.MC",
    "ACX.MC", "AENA.MC", "ALM.MC", "BKT.MC", "CABK.MC",
    "COL.MC", "ENG.MC", "GRF.MC", "IAG.MC", "MAP.MC",
    # Nasdaq
    "AAPL", "MSFT", "NVDA", "GOOGL", "META",
    "AMZN", "TSLA", "AMD", "INTC", "NFLX",
    "PYPL", "ADBE", "CRM", "QCOM", "TXN",
    "ASML", "MU", "AMAT", "LRCX", "KLAC",
    # ETFs
    "SPY", "QQQ", "VTI", "EWP", "IEMG",
    # Crypto
    "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"
]

def download_data(tickers, period="2y"):
    all_data = []
    
    for ticker in tickers:
        print(f"Descargando {ticker}...")
        df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None
        df["ticker"] = ticker
        df["extracted_at"] = datetime.now(timezone.utc)
        all_data.append(df)
    
    return pd.concat(all_data).reset_index()

if __name__ == "__main__":
    print("Iniciando descarga de datos...")
    df = download_data(TICKERS)
    print(f"Descarga completada. {len(df)} filas descargadas.")
    print(df.head())