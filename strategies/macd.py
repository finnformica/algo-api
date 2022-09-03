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

    df['ema_12'] = df.Close.ewm(span=12).mean()
    df['ema_26'] = df.Close.ewm(span=26).mean()
    df['macd'] = df.ema_12 - df.ema_26
    df['signal'] = df.macd.ewm(span=9).mean()

    df.dropna(inplace=True)
    
    return convert_to_json(
        df,
        'oscillator',
        ticker,
        start,
        macd=df.macd,
        signal=df.signal
    )
