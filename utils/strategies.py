import yfinance as yf
import pandas as pd
import numpy as np
import ta
pd.options.mode.chained_assignment = None

from core.config import responses

def calculate_pnl(sellprices, buyprices):
    return (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1

def mean_reversion_bollinger_band(ticker, start, stop_loss):
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
    
    return {
        'data': {
            'close': df.Close,
            'upper_bb': df.upper_bb,
            'lower_bb': df.lower_bb
        },
        'positions': {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        'info': {
            'ticker': ticker,
            'startdate': start,
            'pnl': calculate_pnl(sellprices, buyprices),
            'type': 'overlay'
        }
    }

def moving_average_crossover(ticker, start, ma_fast, ma_slow):
    df = yf.download(ticker, start=start)

    if df.empty:
        return responses.INVALID_TICKER
    
    df['ma_fast'] = df.Close.rolling(ma_fast).mean()
    df['ma_slow'] = df.Close.rolling(ma_slow).mean()
    df.dropna(inplace=True)

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for i in range(len(df)):
        if not position:
            if df.ma_fast.iloc[i] > df.ma_slow.iloc[i] and df.ma_fast.iloc[i - 1] < df.ma_slow.iloc[i - 1]:
                
                buydates.append(df.index[i])
                buyprices.append(df.Open[i])
                position = True
        
        if position:
            if df.ma_fast.iloc[i] < df.ma_slow.iloc[i] and df.ma_fast.iloc[i - 1] > df.ma_slow.iloc[i - 1]:
                selldates.append(df.index[i])
                sellprices.append(df.Open[i])
                position = False
    
    return {
        'data': {
            'close': df.Close,
            'ma_fast': df.ma_fast,
            'ma_slow': df.ma_slow
        },
        'positions': {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        'info': {
            'ticker': ticker,
            'startdate': start,
            'pnl': calculate_pnl(sellprices, buyprices),
            'type': 'overlay'
        }
    }

def macd(ticker, start):
    df = yf.download(ticker, start=start)

    df['ema_12'] = df.Close.ewm(span=12).mean()
    df['ema_26'] = df.Close.ewm(span=26).mean()
    df['macd'] = df.ema_12 - df.ema_26
    df['signal'] = df.macd.ewm(span=9).mean()

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for i in range(2, len(df)):
        if not position:
            if df.macd.iloc[i] > df.signal.iloc[i] and df.macd.iloc[i - 1] < df.signal.iloc[i - 1]:
                buydates.append(df.index[i])
                buyprices.append(df.Open[i])
                position = True
        
        if position:
            if df.macd.iloc[i] < df.signal.iloc[i] and df.macd.iloc[i - 1] > df.signal.iloc[i - 1]:
                selldates.append(df.index[i])
                sellprices.append(df.Open[i])
                position = False
    
    return {
        'data': {
            'close': df.Close,
            'macd': df.macd,
            'signal': df.signal
        },
        'positions': {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        'info': {
            'ticker': ticker,
            'startdate': start,
            'pnl': calculate_pnl(sellprices, buyprices),
            'type': 'oscillator'
        }
    }


def supertrend(ticker, start, period, multiplier):
    df = yf.download(ticker, start=start)

    # calculate true range
    df['previous_close'] = df.Close.shift()
    df['H-L'] = df.High - df.Low
    df['H-Cp'] = abs(df.High - df.previous_close)
    df['L-Cp'] = abs(df.Low - df.previous_close)
    df.dropna(inplace=True)
    df['tr'] = df[['H-L', 'H-Cp', 'L-Cp']].max(axis=1)

    # calculate average true range
    df['atr'] = df['tr'].rolling(14).mean()

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

    return {
        'data': {
            'close': df.Close,
            'upperband': df.upperband,
            'lowerband': df.lowerband
        },
        'positions': {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        },
        'info': {
            'ticker': ticker,
            'startdate': start,
            'pnl': calculate_pnl(sellprices, buyprices),
            'type': 'overlay'
        }
    }