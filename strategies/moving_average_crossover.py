import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def _moving_average_crossover(ticker, start, ma_fast, ma_slow):
    df = yf.download(ticker, start=start)

    if df.empty:
        return response_invalid(ticker)
    
    df['ma_fast'] = df.Close.rolling(ma_fast).mean()
    df['ma_slow'] = df.Close.rolling(ma_slow).mean()

    df.dropna(inplace=True)
    
    return convert_to_json(
        type='overlay',
        ticker=ticker,
        start=start,
        close=df.Close,
        ma_fast=df.ma_fast,
        ma_slow=df.ma_slow
    )
