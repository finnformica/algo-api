from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from core.config import settings

import strategies

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/average-true-range")
def average_true_range(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return strategies.average_true_range.index(ticker, start, int(period))

@app.get("/bollinger-band")
def bollinger_band(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE):
    return strategies.bollinger_band.index(ticker, start)

@app.get("/ichimoku-cloud")
def ichimoku_cloud(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE):
    return strategies.ichimoku_cloud.index(ticker, start)

@app.get("/macd")
def macd(ticker=settings.DEFAULT_TICKER, start="2022-01-01"):
    return strategies.macd.index(ticker, start)

@app.get("/moving-average-crossover")
def moving_average_crossover(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, ma_fast=20, ma_slow=50):
    return strategies.moving_average_crossover.index(ticker, start, int(ma_fast), int(ma_slow))

@app.get("/rsi")
def rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return strategies.rsi.index(ticker, start, int(period))

@app.get("/stochastic-oscillator")
def stochastic_oscillator(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return strategies.stochastic_oscillator.index(ticker, start, int(period))

@app.get("/stochastic-rsi")
def stochastic_rsi(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return strategies.stochastic_rsi.index(ticker, start, int(period))

@app.get("/supertrend")
def supertrend(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14, multiplier=2.5):
    return strategies.supertrend.index(ticker, start, int(period), float(multiplier))

@app.get("/volatility")
def volatility(ticker=settings.DEFAULT_TICKER, start=settings.DEFAULT_STARTDATE, period=14):
    return strategies.volatility.index(ticker, start, int(period))

# fear and greed
# Keltner Channel
# Market Liberator
# Market Cipher
# VuManChu Cipher
# ADX
#