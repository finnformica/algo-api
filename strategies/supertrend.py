import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import convert_to_json, response_invalid

def index(ticker, start, period, multiplier):
    df = yf.download(ticker, start=start)

    if df.empty:
        return response_invalid(ticker)

    # calculate true range
    df['previous_close'] = df.Close.shift()
    df['H-L'] = df.High - df.Low
    df['H-Cp'] = abs(df.High - df.previous_close)
    df['L-Cp'] = abs(df.Low - df.previous_close)

    df['tr'] = df[['H-L', 'H-Cp', 'L-Cp']].max(axis=1)

    # calculate average true range
    df['atr'] = df['tr'].rolling(int(period)).mean()

    # calculate basic upper and lower bands
    df['upperband'] = ((df.High + df.Low) / 2) + (multiplier * df['atr'])
    df['lowerband'] = ((df.High + df.Low) / 2) - (multiplier * df['atr'])

    df.dropna(inplace=True)

    df['in_uptrend'] = True

    # calculate supertrend upper and lower bands and generate buy / sell signals
    for i in range(len(df)):
        if df.Close.iloc[i] > df.upperband.iloc[i-1]:
            df.in_uptrend.iloc[i] = True
        
        elif df.Close.iloc[i] < df.lowerband.iloc[i-1]:
            df.in_uptrend.iloc[i] = False
        
        else:
            df.in_uptrend.iloc[i] = df.in_uptrend.iloc[i-1]

            if df.in_uptrend.iloc[i] and df.lowerband.iloc[i] < df.lowerband.iloc[i-1]:
                df.lowerband.iloc[i] = df.lowerband.iloc[i-1]

            if not df.in_uptrend.iloc[i] and df.upperband.iloc[i] > df.upperband.iloc[i-1]:
                df.upperband.iloc[i] = df.upperband.iloc[i-1]


    return convert_to_json(
        df,
        'overlay',
        ticker,
        start,
        upperband=df.upperband,
        lowerband=df.lowerband
    )
    