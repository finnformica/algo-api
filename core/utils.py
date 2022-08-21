import pandas as pd

def calculate_pnl(sellprices, buyprices):
    return (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1

def generate_buy_sell_dates(df, column1, column2, stop_loss):
    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for i in range(2, len(df)):
        if not position:
            if df[column1].iloc[i] > df[column2].iloc[i] and df[column1].iloc[i-1] < df[column2].iloc[i-1]:
                buydates.append(df.index[i])
                buyprices.append(df.Open.iloc[i])
                position = True
        
        if position:
            if df[column1].iloc[i] < df[column2].iloc[i] and df[column1].iloc[i-1] > df[column2].iloc[i-1] or df.Close.iloc[i] < (1 - int(stop_loss)) * buyprices[-1]:
                selldates.append(df.index[i])
                sellprices.append(df.Open.iloc[i])
                position = False
    
    return {
            'buydates': buydates,
            'selldates': selldates,
            'buyprices': buyprices,
            'sellprices': sellprices
        }

def convert_to_json(type, ticker, start, positions, **kwargs):
    if positions:
        return {
            'data': { key: value for key, value in kwargs.items()},
            'positions': positions,
            'info': {
                'ticker': ticker,
                'startdate': start,
                'pnl': calculate_pnl(positions['sellprices'], positions['buyprices']),
                'type': type
            }
        }
    
    else:
        return {
            'data': { key: value for key, value in kwargs.items()},
            'info': {
                'ticker': ticker,
                'startdate': start,
                'type': type
            }
        }
