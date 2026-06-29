import pandas as pd

source = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
sp500 = pd.read_csv(source)
sp500 = sp500[['Symbol', 'Security']].rename(columns={'Symbol':'ticker', 'Security':'name'})
sp500.to_csv("sp500_list.csv", index = False)
print(f"saved{len(sp500)} tickers")