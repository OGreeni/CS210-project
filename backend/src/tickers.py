import os
import pandas as pd
import re


def find_tickers(string):
    tickers_found = []

    current_dir = os.path.dirname(__file__)

    csv_path = os.path.join(current_dir, '../us_symbols.csv')

    df = pd.read_csv(csv_path)
    tickers = df['ticker']

    for ticker in tickers:
        # TODO: refine this search. Some tickers are also actual words (i.e., 'A' and 'AM'), so we need to work
        #  around that
        if re.search(f' {ticker} ', string):
            tickers_found.append(ticker)

    return tickers_found
