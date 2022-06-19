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


@app.get("/company-info/{ticker}")
def read_company_info(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    company_info_key = f"{ticker}_company_info"
    company_info = redis_client.get(company_info_key)

    if company_info is None:
        print("Retrieving data from API...")
        company_info = stock.get_company_info()
        redis_client.set(company_info_key, json.dumps(company_info))
    else:
        print("Retrieving data from cache...")
        company_info = json.loads(company_info)

    return json.dumps(company_info)


@app.get("/stats/{ticker}")
def read_stats(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    stats_info_key = f"{ticker}_stats"
    stats = redis_client.get(stats_info_key)

    if stats is None:
        print("Retrieving data from API...")
        stats = stock.get_stats()
        redis_client.set(stats_info_key, json.dumps(stats))
    else:
        print("Retrieving data from cache...")
        stats = json.loads(stats)

    return json.dumps(stats)


# Can also handle a request for any amount of news posts
@app.get("/news/{ticker}")
def read_news(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    news_info_key = f"{ticker}_news"
    news = redis_client.get(news_info_key)

    if news in None:
        print("Retrieving data from API...")
        news = stock.get_company_news()
        redis_client.set(news_info_key, json.dumps(news))
    else:
        print("Retrieving data from cache...")
        stats = json.loads(news)

    return json.dumps(news)


# Can also specify range (in years) of news to gather
@app.get("/dividends/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    dividends_info_key = f"{ticker}_news"
    dividends = redis_client.get(dividends_info_key)

    if dividends in None:
        print("Retrieving data from API...")
        dividends = stock.get_dividends()
        redis_client.set(dividends_info_key, json.dumps(dividends))
    else:
        print("Retrieving data from cache...")
        dividends = json.loads(dividends)

    return json.dumps(dividends)


@app.get("/institutional-ownership/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    institutional_ownership_info_key = f"{ticker}_news"
    institutional_ownership = redis_client.get(institutional_ownership_info_key)

    if institutional_ownership in None:
        print("Retrieving data from API...")
        institutional_ownership = stock.get_institutional_ownership()
        redis_client.set(institutional_ownership_info_key, json.dumps(institutional_ownership))
    else:
        print("Retrieving data from cache...")
        institutional_ownership = json.loads(institutional_ownership)

    return json.dumps(institutional_ownership)


@app.get("/insider-transactions/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    insider_transactions_info_key = f"{ticker}_news"
    insider_transactions = redis_client.get(insider_transactions_info_key)

    if insider_transactions in None:
        print("Retrieving data from API...")
        insider_transactions = stock.get_insider_transactions()
        redis_client.set(insider_transactions_info_key, json.dumps(insider_transactions))
    else:
        print("Retrieving data from cache...")
        insider_transactions = json.loads(insider_transactions)

    return json.dumps(insider_transactions)