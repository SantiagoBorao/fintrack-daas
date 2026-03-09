# FinTrack DaaS — Financial Data Platform

> 🚧 Work in progress — actively being built

My idea is to create a batch data pipeline that detects volume anomalies and moving 
average signals across IBEX 35, Nasdaq stocks and ETFs.

## What this will do
- Download daily OHLCV data for 50 tickers using yfinance
- Store raw data in Google BigQuery
- Calculate SMA 50/200, Golden Cross signals and volume 
  anomaly flags using dbt
- Serve insights through a Streamlit dashboard

## Planned architecture

Yahoo Finance → Python → BigQuery (Raw) → dbt → Streamlit

## Tech stack

- Python + yfinance
- Google BigQuery
- dbt
- Streamlit

## Status

| Phase | Status |
|-------|--------|
| Phase 1 — Data collector | 🔄 In progress |
| Phase 2 — BigQuery setup | ⏳ Pending |
| Phase 3 — dbt transforms | ⏳ Pending |
| Phase 4 — Streamlit dashboard | ⏳ Pending |

## Author
[Tu nombre] — [tu web]
