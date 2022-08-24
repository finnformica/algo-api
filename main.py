from fastapi import FastAPI
from core.config import settings

from strategies.average_true_range import _average_true_range
from strategies.bollinger_band import _bollinger_band
from strategies.ichimoku_cloud import _ichimoku_cloud
from strategies.macd import _macd
from strategies.moving_average_crossover import _moving_average_crossover
from strategies.rsi import _rsi
from strategies.stochastic_oscillator import _stochastic_oscillator
from strategies.stochastic_rsi import _stochastic_rsi
from strategies.supertrend import _supertrend
from strategies.volatility import _volatility

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

@app.get("/average-true-range")
def average_true_range(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return _average_true_range(ticker, start, int(period))

@app.get("/bollinger-band")
def bollinger_band(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE):
    return _bollinger_band(ticker, start)

@app.get("/ichimoku-cloud")
def ichimoku_cloud(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE):
    return _ichimoku_cloud(ticker, start)

@app.get("/macd")
def macd(ticker=settings.DEFAULT_TICKER, start="2022-01-01"):
    return _macd(ticker, start)

@app.get("/moving-average-crossover")
def moving_average_crossover(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, ma_fast=20, ma_slow=50):
    return _moving_average_crossover(ticker, start, int(ma_fast), int(ma_slow))

@app.get("/rsi")
def rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return _rsi(ticker, start, int(period))

@app.get("/stochastic-oscillator")
def stochastic_oscillator(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return _stochastic_oscillator(ticker, start, int(period))

@app.get("/stochastic-rsi")
def stochastic_rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return _stochastic_rsi(ticker, start, int(period))

@app.get("/supertrend")
def supertrend(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, multiplier=2.5):
    return _supertrend(ticker, start, int(period), float(multiplier))

@app.get("/volatility")
def volatility(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return _volatility(ticker, start, int(period))

# fear and greed
# Keltner Channel
