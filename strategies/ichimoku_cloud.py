import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def index(ticker, start):
    df = yf.download(ticker, start=start)

    if df.empty:
        return response_invalid(ticker)

    df['conversion'] = (df.Close.rolling(9).max() + df.Close.rolling(9).min()) / 2
    df['base'] = (df.Close.rolling(26).max() + df.Close.rolling(26).min()) / 2
    df['leading_a'] = ((df.conversion + df.base) / 2).shift(26)
    df['leading_b'] = ((df.Close.rolling(52).max() + df.Close.rolling(52).min()) / 2).shift(26)

    df.dropna(inplace=True)

    return convert_to_json(
        df,
        type='overlay',
        ticker=ticker,
        start=start,
        name="ichimoku-cloud",
        leading_a=df.leading_a,
        leading_b=df.leading_b
    ) 
