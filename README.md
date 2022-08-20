# algo-api

## Introduction

An API to generate buy and sell signals for a stock based on a particular strategy. This will be used as a backend to serve a front-end dashboard.

## Dependencies

- Python 3.7.2+
- pip 21.0.1+

## Getting Started

1. Clone the repository

```bash
git clone https://github.com/finnformica/algo-api.git
```

2. Create the virtual environment, e.g. (for macOS)

```
cd /.../algo-api/
```

```
python3 -m venv venv
```

```
source venv/bin/activate
```

3. Install requirements

```
pip3 install requirements.txt
```

4. Run app

```
uvicorn main:app --reload
```

5. Navigate to **localhost:8000**

## Features

- FastAPI app
- Microservice architecture
- Retrieves up to date data using yfinance
