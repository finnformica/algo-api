from fastapi import FastAPI
from core.config import settings
import utils.strategies

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

@app.get("/macd")
def macd(ticker="MSFT", start="2022-01-01"):
    return utils.strategies.macd(ticker, start)

@app.get("/mean-reversion-bollinger-band")
def mean_reversion_bollinger_band(ticker="MSFT", start="2019-01-01", stop_loss=0.05):
    return utils.strategies.mean_reversion_bollinger_band(ticker, start, stop_loss)

@app.get("/moving-average-crossover")
def moving_average_crossover(ticker="MSFT", start="2019-01-01", ma_fast=20, ma_slow=50):
    return utils.strategies.moving_average_crossover(ticker, start, ma_fast, ma_slow)

@app.get("/supertrend")
def supertrend(ticker="MSFT", start="2019-01-01", period=14, multiplier=2.5):
    return utils.strategies.supertrend(ticker, start, period, multiplier)