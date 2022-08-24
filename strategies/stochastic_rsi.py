import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def _stochastic_rsi(ticker, start, period):
    df = yf.download(ticker, start=start)
    
    if df.empty:
        return response_invalid(ticker)

    df['rsi'] = ta.momentum.rsi(df.Close, window=period)

    df['period_low'] = df.rsi.rolling(period).min()
    df['period_high'] = df.rsi.rolling(period).max()

    df['stochastic_rsi_k'] = (100 * (df.rsi - df.period_low) / (df.period_high - df.period_low)).rolling(3).mean()
    df['stochastic_rsi_d'] = df.stochastic_rsi_k.rolling(3).mean()

    df.dropna(inplace=True)

    return convert_to_json(
        'oscillator',
        ticker,
        start,
        positions=False,
        close=df.Close,
        k=df.stochastic_rsi_k,
        d=df.stochastic_rsi_d
    )
