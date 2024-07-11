import pandas as pd


def read_tickers():
    df = pd.read_csv('../tickers.csv')
    tickers = df['ticker']
