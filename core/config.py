class Settings:
    PROJECT_NAME: str = "Algo API"
    PROJECT_VERSION: str = "1.0.0"
    DEFAULT_TICKER: str = "MSFT"
    DEFAULT_STARTDATE: str = "2019-01-01"
    DEFAULT_STOPLOSS: int = 1

class Responses:
    INVALID_TICKER: str = "Response invalid for ticker"

settings = Settings()
responses = Responses()