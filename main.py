"""
Steps to run in a venv:

python -m venv .venv
source .venv/bin/activate
pip install uvicorn
pip install fastapi
pip install redis
pip install requests
uvicorn main:app --reload
"""

from fastapi import FastAPI
import config
import redis
import json
from iex_service import IEXStock

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/logo/{ticker}")
def read_logo(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    logo_key = f"{ticker}_logo"
    logo = redis_client.get(logo_key)

    if logo is None:
        print("Retrieving data from API...")
        logo = stock.get_logo()
        redis_client.set(logo_key, json.dumps(logo))
    else:
        print("Retrieving data from cache...")
        logo = json.loads(logo)

    return json.dumps(logo)
