import itertools
import pandas as pd
import streamlit as st
from data import load_prices, USED_TICKERS, CLUSTER_LABELS

@st.cache_data
def load_sp500_list():
    return pd.read_csv('sp500_list.csv')

def takeaway(corr):
    if corr > 0.7:
        return "Highly correlated"
    elif corr > 0.3:
        return "moderatley correlated"
    elif corr > -0.3:
        return "not correlated"
    else:
        return "move in opposite directions"

st.set_page_config(page_title = "Portfolio correlation checker", layout = "centered")
st.title("Portfolio correlation checker")
st.write("pick some stocks and check if your portfolio is well diversified")

sp500 = load_sp500_list()
label_to_ticker = {f"{row.ticker}-{row.name}": row.ticker for row in sp500.itertuples()}
options = sorted(label_to_ticker.keys())
default_labels = [l for l in options if l.split('-')[0] in USED_TICKERS[:2]]

selected_label = st.multiselect("select stocks ", options, default=default_labels)
selected = [label_to_ticker[l] for l in selected_label]



if len(selected) < 2:
    st.info("selct more than 2 stocks")
else:
    with st.spinner("fetching price history..."):
        close = load_prices(selected)
    returns = close.pct_change().dropna()

    corr_matrix = returns[selected].corr()
    vol = returns[selected].std()*(252**0.5)

    st.subheader("Correlation")
    st.dataframe(corr_matrix.style.background_gradient(cmap='RdYlGn_r', vmin=-1, vmax=1))

    st.subheader("Volatility(annualized)")
    st.bar_chart(vol)

    st.subheader("Behavioural cluster")
    for t in selected:
        st.write(f"--{t}--: {CLUSTER_LABELS.get(t, 'Not yet classified')}")

    st.subheader("Takeaway")
    for s1, s2 in itertools.combinations(selected,2):
        c = corr_matrix.loc[s1,s2]
        st.write(f"--{s1} & {s2}--({c:.2f}) - {takeaway(c)}")

