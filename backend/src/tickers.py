import os
import pandas as pd
import re


def find_tickers(string):
    tickers_found = []

    current_dir = os.path.dirname(__file__)

    csv_path = os.path.join(current_dir, '..', 'us_symbols.csv')

    df = pd.read_csv(csv_path)
    tickers = df['ticker']

    for ticker in tickers:
        # Note: only searching for tickers containing 4 letters.
        if len(ticker) != 4:
            continue

        if re.search(str(ticker), string):
            tickers_found.append(ticker)

    return tickers_found
