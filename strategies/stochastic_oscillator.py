import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def _stochastic_oscillator(ticker, start, period):
    df = yf.download(ticker, start=start)

    if df.empty:
        return response_invalid(ticker)

    df['period_low'] = df.Low.rolling(period).min()
    df['period_high'] = df.High.rolling(period).max()

    df['stoch_oscillator'] = (df.Close - df.period_low) / (df.period_high - df.period_low)

    df.dropna(inplace=True)

    return convert_to_json(
        'oscillator',
        ticker,
        start,
        positions=False,
        close=df.Close,
        stoch_oscillator=df.stoch_oscillator
    )
