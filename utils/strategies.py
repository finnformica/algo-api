import yfinance as yf
import pandas as pd
import numpy as np
import ta

from core.config import responses

def mean_reversion_bollinger_band(ticker, start):
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
            if row['signal'] == 'Sell' or row.shifted_close < 0.95 * buyprices[-1]:
                selldates.append(index)
                sellprices.append(row.Open)
                position = False
    
    return {
        'close': df.Close,
        'buydates': buydates,
        'selldates': selldates,
        'buyprices': buyprices,
        'sellprices': sellprices,
        'ticker': ticker,
        'startdate': start
    }

def moving_average_crossover(ticker, start):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER
    
    df['ma_20'] = df.Close.rolling(20).mean()
    df['ma_50'] = df.Close.rolling(50).mean()
    df.dropna(inplace=True)

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for i in range(len(df)):
        print(i)
        if not position:
            if df.ma_20.iloc[i] > df.ma_50.iloc[i] and df.ma_20.iloc[i - 1] < df.ma_50.iloc[i - 1]:
                
                buydates.append(df.index[i])
                buyprices.append(df.Open[i])
                position = True
        
        if position:
            if df.ma_20.iloc[i] < df.ma_50.iloc[i] and df.ma_20.iloc[i - 1] > df.ma_50.iloc[i - 1]:
                selldates.append(df.index[i])
                sellprices.append(df.Open[i])
                position = False
    
    return {
        'close': df.Close,
        'buydates': buydates,
        'selldates': selldates,
        'buyprices': buyprices,
        'sellprices': sellprices,
        'ticker': ticker,
        'startdate': start
    }