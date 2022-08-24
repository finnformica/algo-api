import pandas as pd

def calculate_pnl(sellprices, buyprices):
    return (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1


def convert_to_json(type, ticker, start, **kwargs):
    return {
        'data': { key: value for key, value in kwargs.items()},
        'info': {
            'ticker': ticker,
            'startdate': start,
            'type': type
        }
    }

def response_invalid(ticker):
    return f"Failed download: No data found for {ticker}, symbol may be delisted from Yahoo Finance"