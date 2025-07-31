import pandas as pd
import numpy as np
from typing import Dict
import os
import glob



def load_orderbook(filepath: str) -> pd.DataFrame:
    """
    Load a CSV in MBP-10 format and reshape the top-N bid/ask levels into list-columns.
    """

    df = pd.read_csv(filepath, header=0)

    # renaming duplicate ts column. MBP-10 has a different name for the first ts(recv)
    if 'ts_event.1' in df.columns:
        df = df.rename(columns={
            'ts_event': 'ts_recv',
            'ts_event.1': 'ts_event'
        })
    else:
        # Fallback if headers differ: pick first two timestamp-like columns
        ts_cols = [c for c in df.columns if 'ts_event' in c or 'ts_recv' in c]
        if len(ts_cols) >= 2:
            df = df.rename(columns={
                ts_cols[0]: 'ts_recv',
                ts_cols[1]: 'ts_event'
            })
    
    df['ts_event'] = pd.to_datetime(df['ts_event'])
    df['ts_recv']  = pd.to_datetime(df['ts_recv'])

    # MBP-10, so we have only 10 levels
    bid_px_cols = [f"bid_px_{i:02d}" for i in range(10)]
    ask_px_cols = [f"ask_px_{i:02d}" for i in range(10)]
    bid_sz_cols = [f"bid_sz_{i:02d}" for i in range(10)]
    ask_sz_cols = [f"ask_sz_{i:02d}" for i in range(10)]

    # lists for prices and sizes
    df['bid_prices'] = df[bid_px_cols].values.tolist()
    df['ask_prices'] = df[ask_px_cols].values.tolist()
    df['bid_sizes']  = df[bid_sz_cols].values.tolist()
    df['ask_sizes']  = df[ask_sz_cols].values.tolist()

    # computing mid_price and spread
    df['mid_price'] = [ (bp[0] + ap[0]) / 2 for bp, ap in zip(df['bid_prices'], df['ask_prices']) ]
    df['spread']    = [ (ap[0] - bp[0])     for bp, ap in zip(df['bid_prices'], df['ask_prices']) ]

    return df    




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
    
    combined_dfs = pd.concat(dfs, ignore_index=True)
    combined_dfs.sort_values("ts_event", inplace=True)
    combined_dfs.reset_index(drop=True, inplace=True)
    return combined_dfs


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