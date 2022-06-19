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
import datetime

from fastapi import FastAPI
import config
import redis
import json
from iex_service import IEXStock

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@app.get("/logo/{ticker}")
def read_logo(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    logo_key = f"{ticker}_logo"
    logo = redis_client.get(logo_key)

    if logo is None:
        print("Retrieving data from API...")
        logo = stock.get_logo()
        redis_client.set(logo_key, json.dumps(logo))
        redis_client.expire(logo_key, datetime.timedelta(days=365))
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
        redis_client.expire(company_info_key, datetime.timedelta(hours=24))
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
        redis_client.expire(stats_info_key, datetime.timedelta(hours=24))
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

    if news is None:
        print("Retrieving data from API...")
        news = stock.get_company_news()
        redis_client.set(news_info_key, json.dumps(news))
        redis_client.expire(news_info_key, datetime.timedelta(hours=1))
    else:
        print("Retrieving data from cache...")
        news = json.loads(news)

    return json.dumps(news)


# Can also specify range (in years) of news to gather
@app.get("/dividends/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    dividends_info_key = f"{ticker}_dividends"
    dividends = redis_client.get(dividends_info_key)

    if dividends is None:
        print("Retrieving data from API...")
        dividends = stock.get_dividends()
        redis_client.set(dividends_info_key, json.dumps(dividends))
        redis_client.expire(dividends_info_key, datetime.timedelta(days=1))
    else:
        print("Retrieving data from cache...")
        dividends = json.loads(dividends)

    return json.dumps(dividends)


@app.get("/institutional-ownership/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    institutional_ownership_info_key = f"{ticker}_institutional-ownership"
    institutional_ownership = redis_client.get(institutional_ownership_info_key)

    if institutional_ownership is None:
        print("Retrieving data from API...")
        institutional_ownership = stock.get_institutional_ownership()
        redis_client.set(institutional_ownership_info_key, json.dumps(institutional_ownership))
        redis_client.expire(institutional_ownership_info_key, datetime.timedelta(days=1))
    else:
        print("Retrieving data from cache...")
        institutional_ownership = json.loads(institutional_ownership)

    return json.dumps(institutional_ownership)


@app.get("/insider-transactions/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(config.IEX_KEY, ticker)
    insider_transactions_info_key = f"{ticker}_insider-transactions"
    insider_transactions = redis_client.get(insider_transactions_info_key)

    if insider_transactions is None:
        print("Retrieving data from API...")
        insider_transactions = stock.get_insider_transactions()
        redis_client.set(insider_transactions_info_key, json.dumps(insider_transactions))
        redis_client.expire(insider_transactions_info_key, datetime.timedelta(days=1))
    else:
        print("Retrieving data from cache...")
        insider_transactions = json.loads(insider_transactions)

    return json.dumps(insider_transactions)


# TODO
# https://iexcloud.io/docs/api/#ceo-compensation
# https://cloud.iexapis.com/stable/time-series/DIVIDENDS_FORECAST/aapl
# https://cloud.iexapis.com/stable/stock/market/today-earnings
# https://cloud.iexapis.com/stable/stock/aapl/fund-ownership ??

