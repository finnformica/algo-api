import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def index(ticker, start, period):
    df = yf.download(ticker, start=start)

    if df.empty:
        return response_invalid(ticker)

    df['stdev'] = df.Close.rolling(period).std()
    df['volatility'] = df.stdev**2

    df.dropna(inplace=True)

    return convert_to_json(
        'oscillator',
        ticker,
        start,
        close=df.Close,
        stdev=df.stdev,
        volatility=df.volatility
    )
