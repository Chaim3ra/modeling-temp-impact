import pandas as pd
import numpy as np
from typing import Dict



def load_orderbook(filepath: str) -> pd.DataFrame:
    """
    Load a CSV in MBP-10 format and reshape the top-N bid/ask levels into list-columns.
    """

    TODO # type: ignore


def load_ticker_data(ticker_dir: str) -> pd.DataFrame:
    """
    Load all CSVs for a single ticker from data directory.
    """

    TODO # type: ignore


def load_tickers(data_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Load orderbook data for all tickers under a base directory(data dir). 
    For now, we have three tickers but this can be accomodate more in the future.
    """


    TODO # type: ignore 