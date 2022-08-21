from lib2to3.pytree import convert
from xml.dom.pulldom import START_ELEMENT
import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.utils import calculate_pnl, generate_buy_sell_dates, convert_to_json
from core.config import responses

def bollinger_band(ticker, start, stop_loss):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER

    df['ma_20'] = df.Close.rolling(20).mean()
    df['vol'] = df.Close.rolling(20).std()
    df['upper_bb'] = df.ma_20 + (2 * df.vol)
    df['lower_bb'] = df.ma_20 - (2 * df.vol)

    df['rsi'] = ta.momentum.rsi(df.Close, window=6)

    conditions = [(df.rsi < 30) & (df.Close < df.lower_bb), 
                (df.rsi > 70) & (df.Close > df.upper_bb)]
    
    choices = ['Buy', 'Sell']

    df['signal'] = np.select(conditions, choices)
    df.dropna(inplace=True)

    df.signal = df.signal.shift()
    df['shifted_close'] = df.Close.shift()

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for index, row in df.iterrows():
        if not position and row['signal'] == 'Buy':
            buydates.append(index)
            buyprices.append(row.Open)
            position = True
        
        if position:
            if row['signal'] == 'Sell' or row.shifted_close < (1 - stop_loss) * buyprices[-1]:
                selldates.append(index)
                sellprices.append(row.Open)
                position = False
    
    return convert_to_json(
        'overlay',
        ticker,
        start,
        {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        close=df.Close,
        upper_bb=df.upper_bb,
        lower_bb=df.lower_bb
    )

def moving_average_crossover(ticker, start, stop_loss, ma_fast, ma_slow):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER
    
    df['ma_fast'] = df.Close.rolling(ma_fast).mean()
    df['ma_slow'] = df.Close.rolling(ma_slow).mean()

    df.dropna(inplace=True)

    positions = generate_buy_sell_dates(df, 'ma_fast', 'ma_slow', stop_loss)
    
    return convert_to_json(
        type='overlay',
        ticker=ticker,
        start=start,
        positions=positions,
        close=df.Close,
        ma_fast=df.ma_fast,
        ma_slow=df.ma_slow
    )

def macd(ticker, start, stop_loss):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER

    df['ema_12'] = df.Close.ewm(span=12).mean()
    df['ema_26'] = df.Close.ewm(span=26).mean()
    df['macd'] = df.ema_12 - df.ema_26
    df['signal'] = df.macd.ewm(span=9).mean()

    df.dropna(inplace=True)

    positions = generate_buy_sell_dates(df, 'macd', 'signal', stop_loss)
    
    return convert_to_json(
        'oscillator',
        ticker,
        start,
        positions,
        close=df.Close,
        macd=df.macd,
        signal=df.signal
    )

def ichimoku_cloud(ticker, start, stop_loss):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER

    df['conversion'] = (df.Close.rolling(9).max() + df.Close.rolling(9).min()) / 2
    df['base'] = (df.Close.rolling(26).max() + df.Close.rolling(26).min()) / 2
    df['leading_a'] = ((df.conversion + df.base) / 2).shift(26)
    df['leading_b'] = ((df.Close.rolling(52).max() + df.Close.rolling(52).min()) / 2).shift(26)

    df.dropna(inplace=True)

    positions = generate_buy_sell_dates(df, 'leading_a', 'leading_b', stop_loss)

    return convert_to_json(
        type='overlay',
        ticker=ticker,
        start=start,
        positions=positions,
        close=df.Close,
        leading_a=df.leading_a,
        leading_b=df.leading_b
    ) 

def supertrend(ticker, start, period, multiplier):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER

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

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    # calculate supertrend upper and lower bands and generate buy / sell signals
    for i in range(len(df)):
        if df.Close.iloc[i] > df.upperband.iloc[i-1] and not position:
            df.in_uptrend.iloc[i] = True

            buydates.append(df.index[i])
            buyprices.append(df.Open.iloc[i])
            position = True
        
        elif df.Close.iloc[i] < df.lowerband.iloc[i-1] and position:
            df.in_uptrend.iloc[i] = False

            selldates.append(df.index[i])
            sellprices.append(df.Open.iloc[i])
            position = False
        
        else:
            df.in_uptrend.iloc[i] = df.in_uptrend.iloc[i-1]

            if df.in_uptrend.iloc[i] and df.lowerband.iloc[i] < df.lowerband.iloc[i-1]:
                df.lowerband.iloc[i] = df.lowerband.iloc[i-1]

            if not df.in_uptrend.iloc[i] and df.upperband.iloc[i] > df.upperband.iloc[i-1]:
                df.upperband.iloc[i] = df.upperband.iloc[i-1]


    return convert_to_json(
        'overlay',
        ticker,
        start,
        {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        close=df.Close,
        upperband=df.upperband,
        lowerband=df.lowerband
    )