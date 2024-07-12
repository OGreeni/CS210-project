import pandas as pd
import re


def find_tickers(string):
    tickers_found = []

    df = pd.read_csv('us_symbols.csv')
    tickers = df['ticker']

    for ticker in tickers:
        # TODO: refine this search. Some tickers are also actual words (i.e., 'A' and 'AM'), so we need to work
        #  around that
        if re.search(f' {ticker} ', string):
            tickers_found.append(ticker)

    return tickers_found
