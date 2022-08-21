from fastapi import FastAPI
from core.config import settings
import core.strategies

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

@app.get("/ichimoku-cloud")
def ichimoku_cloud(ticker="MSFT", start="2019-01-01", stop_loss=1):
    return core.strategies.ichimoku_cloud(ticker, start, float(stop_loss))

@app.get("/macd")
def macd(ticker="MSFT", start="2022-01-01", stop_loss=0.05):
    return core.strategies.macd(ticker, start, float(stop_loss))

@app.get("/mean-reversion-bollinger-band")
def mean_reversion_bollinger_band(ticker="MSFT", start="2019-01-01", stop_loss=0.05):
    return core.strategies.mean_reversion_bollinger_band(ticker, start, float(stop_loss))

@app.get("/moving-average-crossover")
def moving_average_crossover(ticker="MSFT", start="2019-01-01", stop_loss=0.05, ma_fast=20, ma_slow=50):
    return core.strategies.moving_average_crossover(ticker, start, float(stop_loss), int(ma_fast), int(ma_slow))

@app.get("/supertrend")
def supertrend(ticker="MSFT", start="2019-01-01", period=14, multiplier=2.5):
    return core.strategies.supertrend(ticker, start, int(period), float(multiplier))