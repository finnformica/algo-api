from fastapi import FastAPI
from core.config import settings
import utils.strategies

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

@app.get("/mean-reversion-bollinger-band")
def mean_reversion_bollinger_band(ticker="MSFT", start="2019-01-01"):
    return utils.strategies.mean_reversion_bollinger_band(ticker, start)
