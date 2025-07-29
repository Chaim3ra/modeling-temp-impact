import pandas as pd
import numpy as np
from typing import Dict
import os
import glob



def load_orderbook(filepath: str) -> pd.DataFrame:
    """
    Load a CSV in MBP-10 format and reshape the top-N bid/ask levels into list-columns.
    """

    df = pd.read_csv(filepath)
    # print(df.head(2))



def load_ticker_data(ticker_dir: str) -> pd.DataFrame:
    """
    Load all CSVs for a single ticker from data directory.
    """

    files = sorted(glob.glob(os.path.join(ticker_dir, "*.csv")))
    dfs = []

    for file in files:
        day_df = load_orderbook(file)
        dfs.append(day_df)
    if not dfs:
        raise FileNotFoundError(f"No CSV files found in {ticker_dir}")
    
    combined = pd.concat(dfs, ignore_index=True)
    combined.sort_values("ts_event", inplace=True)
    combined.reset_index(drop=True, inplace=True)
    return combined


def load_tickers(data_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Load orderbook data for all tickers under a base directory(data dir). 
    For now, we have three tickers but this can accomodate more in the future.
    """

    tickers = {}

    for entry in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, entry)

        if os.path.isdir(path):
            df = load_ticker_data(path)
            tickers[entry] = df

    if not tickers:
        raise FileNotFoundError(f"No ticker subdirectories found in {data_dir}")
    return tickers



# testing
if __name__ == "__main__":
    load_tickers("data/")