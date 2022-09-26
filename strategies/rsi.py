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

    df['delta'] = df.Close.diff(1)

    up = df.delta.copy()
    down = df.delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    df['up'] = up
    df['down'] = down

    df['avg_gain'] = df.up.rolling(period).mean()
    df['avg_loss'] = abs(df.down.rolling(period).mean())
    df['relative_strength'] = df.avg_gain / df.avg_loss

    df['rsi'] = 100 - (100 / (1 + df.relative_strength))

    df.dropna(inplace=True)
    
    return convert_to_json(
        df,
        'oscillator',
        ticker,
        start,
        "rsi",
        rsi=df.rsi
    )
