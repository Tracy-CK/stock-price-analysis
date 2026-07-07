# S&P 500 Stock Behavior & Risk Analysis for Diversification

A Python-based data science project exploring whether holding stocks from different sectors actually means you're diversified 

## What this project does

Analyses six S&P 500 companies — Apple, NVIDIA, JPMorgan, ExxonMobil, Amazon, and Lockheed Martin — across six techniques:

- **EDA** — price trends, returns, volatility
- **Anomaly Detection** — relative (z-score) vs absolute (5% threshold) unusual moves
- **Correlation Analysis** — testing whether economically-linked stocks actually move together
- **Clustering** — grouping stocks by behavior, not by sector
- **Forecasting** — ARIMA with confidence intervals calibrated by cluster
- **Association Rule Mining** — Apriori on daily up/down moves

## Key finding

Most co-movement between these stocks reflects broad market sentiment, not specific business relationships. Diversification tends to fail exactly when you need it most.

## Interactive app

[Portfolio Correlation Checker] — pick any S&P 500 stocks and see whether your portfolio is genuinely diversified.

## Tech stack

Python · Pandas · yfinance · Scikit-learn · Statsmodels · Mlxtend · Plotly · Streamlit · SQLite

## Structure

| File | Purpose |
|---|---|
| `stock_analysis.ipynb` | Full analysis notebook |
| `app.py` | Streamlit web app |
| `data.py` | Data fetching and SQLite caching |
| `sp500_list.csv` | S&P 500 ticker reference list |
