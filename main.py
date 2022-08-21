from multiprocessing import parent_process
from fastapi import FastAPI
from core.config import settings
import core.strategies

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

@app.get("/average-true-range")
def average_true_range(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE):
    return core.strategies.average_true_range(ticker, start)

@app.get("/bollinger-band")
def bollinger_band(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.bollinger_band(ticker, start, float(stop_loss))

@app.get("/ichimoku-cloud")
def ichimoku_cloud(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.ichimoku_cloud(ticker, start, float(stop_loss))

@app.get("/macd")
def macd(ticker=settings.DEFAULT_TICKER, start="2022-01-01", stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.macd(ticker, start, float(stop_loss))

@app.get("/moving-average-crossover")
def moving_average_crossover(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, stop_loss=settings.DEFAULT_STOPLOSS, ma_fast=20, ma_slow=50):
    return core.strategies.moving_average_crossover(ticker, start, float(stop_loss), int(ma_fast), int(ma_slow))

@app.get("/rsi")
def rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.rsi(ticker, start, int(period), float(stop_loss))

@app.get("/stochastic-oscillator")
def stochastic_oscillator(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.stochastic_oscillator(ticker, start, int(period))

@app.get("/stochastic-rsi")
def stochastic_rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, stop_loss=settings.DEFAULT_STOPLOSS):
    return core.strategies.stochastic_rsi(ticker, start, int(period))

@app.get("/supertrend")
def supertrend(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, multiplier=2.5):
    return core.strategies.supertrend(ticker, start, int(period), float(multiplier))


# fear and greed
# volatility