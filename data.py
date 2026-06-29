import sqlite3
import pandas as pd
import yfinance as yf

DB_PATH = "stocks_cache.db"
USED_TICKERS = ['AAPL','NVDA', 'JPM','XOM','AMZN','LMT']
CLUSTER_LABELS = {t: "TBD" for t in USED_TICKERS}
def connect():
    return sqlite3.connect(DB_PATH)

def table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS prices(date TEXT, ticker TEXT , close REAL, PRIMARY KEY(date,ticker))''')

def cached_tickers(conn):
    try: 
        return set(pd.read_sql("SELECT DISTINCT ticker FROM prices", conn)['ticker'])
    except Exception:
        return set()

def cache_stale(conn, ticker, max_age_days=1):
    try:
        last_date = pd.read_sql("SELECT MAX(date) as d FROM prices WHERE ticker = ?", conn, params =(ticker,))['d'][0]
        return last_date is None or (pd.Timestamp.today() - pd.Timestamp(last_date)).days > max_age_days
    except Exception:
        return True

def refresh_cache(conn,tickers):
    data = yf.download(tickers, start='2020-01-01', threads=False)
    close = data['Close']
    if isinstance(close, pd.Series):
             close = close.to_frame(name=tickers[0])
    long = (close.reset_index()
             .melt(id_vars='Date',var_name='ticker', value_name='close')
             .rename(columns={'Date':'date'}))
    long['date']= long['date'].astype(str)
    long.to_sql('prices', conn, if_exists='append', index=False)

def load_prices(tickers):
    conn = connect()
    table(conn)
    
    cached = cached_tickers(conn)
    fetch = [t for t in tickers if t not in cached or cache_stale(conn, t)]

    if fetch:
        conn.execute(
            f"DELETE FROM prices WHERE ticker IN ({','.join('?'*len(fetch))})", fetch)
        refresh_cache(conn, fetch)
    
    placeholders = ','.join('?' * len(tickers))
    df = pd.read_sql(f"SELECT * FROM prices WHERE ticker IN ({placeholders})", conn, params=tickers, parse_dates=['date'])
    
    conn.close()
    return df.pivot(index= 'date', columns='ticker', values='close')


    