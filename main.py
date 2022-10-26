"""
Steps to run in a venv:

python -m venv .venv
source .venv/bin/activate
pip install uvicorn
pip install fastapi
pip install redis
pip install ...
uvicorn main:app --reload
"""
from datetime import datetime, timedelta
import json
import pandas
import random
import uvicorn
from urllib.parse import urlencode
from urllib.request import urlopen

import redis
from fastapi import FastAPI
import yahoo_fin.stock_info as si

import os

from currency import *
from iex_service import IEXStock

app = FastAPI()
redis_client = redis.Redis(host='alek-redis', port=6379, db=0)


@app.get("/logo/{ticker}")
def read_logo(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    logo_key = f"{ticker}_logo"
    logo = redis_client.get(logo_key)

    if logo is None:
        logo = stock.get_logo()
        redis_client.set(logo_key, json.dumps(logo))
        redis_client.expire(logo_key, timedelta(days=365))
        print(f"Retrieved {logo} from the API")
    else:
        logo = json.loads(logo)
        print(f"Retrieved {logo} from cache")

    return logo


@app.get("/company-info/{ticker}")
def read_company_info(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    company_info_key = f"{ticker}_company_info"
    company_info = redis_client.get(company_info_key)

    if company_info is None:
        company_info = stock.get_company_info()
        redis_client.set(company_info_key, json.dumps(company_info))
        redis_client.expire(company_info_key, timedelta(hours=24))
        print(f"Retrieved {company_info} from the API")
    else:
        company_info = json.loads(company_info)
        print(f"Retrieved {company_info} from cache")

    return company_info


@app.get("/stats/{ticker}")
def read_stats(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    stats_info_key = f"{ticker}_stats"
    stats = redis_client.get(stats_info_key)

    if stats is None:
        stats = stock.get_stats()
        redis_client.set(stats_info_key, json.dumps(stats))
        redis_client.expire(stats_info_key, timedelta(hours=24))
        print(f"Retrieved {stats} from the API")
    else:
        stats = json.loads(stats)
        print(f"Retrieved {stats} from cache")

    return stats


# Can also handle a request for any amount of news posts
@app.get("/news/{ticker}")
def read_news(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    news_info_key = f"{ticker}_news"
    news = redis_client.get(news_info_key)

    if news is None:
        news = stock.get_company_news()
        redis_client.set(news_info_key, json.dumps(news))
        redis_client.expire(news_info_key, timedelta(hours=1))
        print(f"Retrieved {news} from the API")
    else:
        news = json.loads(news)
        print(f"Retrieved {news} from cache")

    return news


# Can also specify range (in years) of news to gather
@app.get("/dividends/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    dividends_info_key = f"{ticker}_dividends"
    dividends = redis_client.get(dividends_info_key)

    if dividends is None:
        dividends = stock.get_dividends()
        redis_client.set(dividends_info_key, json.dumps(dividends))
        redis_client.expire(dividends_info_key, timedelta(days=1))
        print(f"Retrieved {dividends} from the API")
    else:
        dividends = json.loads(dividends)
        print(f"Retrieved {dividends} from cache")

    return dividends


@app.get("/institutional-ownership/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    institutional_ownership_info_key = f"{ticker}_institutional-ownership"
    institutional_ownership = redis_client.get(institutional_ownership_info_key)

    if institutional_ownership is None:
        institutional_ownership = stock.get_institutional_ownership()
        redis_client.set(institutional_ownership_info_key, json.dumps(institutional_ownership))
        redis_client.expire(institutional_ownership_info_key, timedelta(days=1))
        print(f"Retrieved {institutional_ownership} from the API")
    else:
        institutional_ownership = json.loads(institutional_ownership)
        print(f"Retrieved {institutional_ownership} from cache")

    return institutional_ownership


@app.get("/insider-transactions/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    insider_transactions_info_key = f"{ticker}_insider-transactions"
    insider_transactions = redis_client.get(insider_transactions_info_key)

    if insider_transactions is None:
        insider_transactions = stock.get_insider_transactions()
        redis_client.set(insider_transactions_info_key, json.dumps(insider_transactions))
        redis_client.expire(insider_transactions_info_key, timedelta(days=1))
        print(f"Retrieved {insider_transactions} from the API")
    else:
        insider_transactions = json.loads(insider_transactions)
        print(f"Retrieved {insider_transactions} from cache")

    return insider_transactions


@app.get("/ceo-compensation/{ticker}")
def read_ceo_compensation(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    ceo_compensation_info_key = f"{ticker}_ceo-compensations"
    ceo_compensation = redis_client.get(ceo_compensation_info_key)

    if ceo_compensation is None:
        ceo_compensation = stock.get_ceo_compensation()
        redis_client.set(ceo_compensation_info_key, json.dumps(ceo_compensation))
        redis_client.expire(ceo_compensation_info_key, timedelta(days=7))
        print(f"Retrieved {ceo_compensation} from the API")
    else:
        ceo_compensation = json.loads(ceo_compensation)
        print(f"Retrieved {ceo_compensation} from cache")

    return ceo_compensation


# @app.get("/today-earnings/")
# def read_today_earnings():
#     stock = IEXStock(os.environ.get('IEX_TOKEN'), None)
#     today_earnings_info_key = "today-earnings"
#     today_earnings = redis_client.get(today_earnings_info_key)
#
#     if today_earnings is None:
#         print("Retrieving data from API...")
#         today_earnings = stock.get_today_earnings()
#         redis_client.set(today_earnings_info_key, json.dumps(today_earnings))
#         redis_client.expire(today_earnings_info_key, timedelta(days=1))
#     else:
#         print("Retrieving data from cache...")
#         today_earnings = json.loads(today_earnings)
#
#     return today_earnings


@app.get("/dividends-forcast/{ticker}")
def read_dividends_forcast(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    dividends_forcast_info_key = f"{ticker}_dividends-forcast"
    dividends_forcast = redis_client.get(dividends_forcast_info_key)

    if dividends_forcast is None:
        print("Retrieving data from API...")
        dividends_forcast = stock.get_dividends_forcast()
        redis_client.set(dividends_forcast_info_key, json.dumps(dividends_forcast))
        redis_client.expire(dividends_forcast_info_key, timedelta(days=7))
    else:
        dividends_forcast = json.loads(dividends_forcast)
        print(f"Retrieved {dividends_forcast} from cache")


    return dividends_forcast


@app.get("/analyst-ratings/{ticker}")
def read_analyst_ratings(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    analyst_ratings_info_key = f"{ticker}_analyst-ratings"
    analyst_ratings = redis_client.get(analyst_ratings_info_key)

    if analyst_ratings is None:
        print("Retrieving data from API...")
        analyst_ratings = stock.get_analyst_ratings()
        redis_client.set(analyst_ratings_info_key, json.dumps(analyst_ratings))
        redis_client.expire(analyst_ratings_info_key, timedelta(days=7))
    else:
        analyst_ratings = json.loads(analyst_ratings)
        print(f"Retrieved {analyst_ratings} from cache")

    print(analyst_ratings)
    return analyst_ratings


# Dummy JSON data for sentiment analysis UI
@app.get("/sentiment/{ticker}/{social_media}")
def read_sentiment(ticker: str, social_media: str):
    return json.loads(json.dumps(
        {'ticker': ticker,
         'socialMedia': social_media,
         'sentimentScore': random.randint(0, 99) + random.randint(0, 10) / 10,
         'itemsScanned': random.randint(100, 999)
         }))


@app.get("/sectors")
def get_sector_data():
    stock = IEXStock(os.environ.get('IEX_TOKEN'), "")
    sector_key = "sector"
    sectors = redis_client.get(sector_key)

    if sectors is None:
        print("Retrieving data from API...")
        sectors = stock.get_sector_data()
        redis_client.set(sector_key, json.dumps(sectors))
        redis_client.expire(sector_key, timedelta(days=1))
    else:
        sectors = json.loads(sectors)
        print(f"Retrieved {sectors} from cache")

    return sectors


@app.get('/currency')
def get_currency_rates():
    return [get_currency_exchange_rates("EUR"), get_currency_exchange_rates("JPY"),
            get_currency_exchange_rates("GBP"), get_currency_exchange_rates("AUD"),
            get_currency_exchange_rates("CAD"), get_currency_exchange_rates("CNY")]


@app.get('/analyst/{ticker}')
def get_analyst_ratings(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), "")
    host = 'https://query2.finance.yahoo.com'
    path = f'/v10/finance/quoteSummary/{ticker}'
    params = {
        'formatted': 'true',
        'lang': 'en-US',
        'region': 'US',
        'modules': 'recommendationTrend'
    }

    response = urlopen('{}{}?{}'.format(host, path, urlencode(params)))
    data = json.loads(response.read().decode())
    print(data)

    return data['quoteSummary']['result']


@app.get('/dividends-history/{ticker}')
def get_dividends_forcast(ticker: str):
    analysts = si.get_analysts_info(ticker)['Earnings History']
    return json.loads(analysts.to_json())


@app.get("/time-series-1d/{ticker}")
def read_dividends_forcast(ticker: str):
    stock = IEXStock(os.environ.get('IEX_TOKEN'), ticker)
    time_series = stock.get_time_series_data()

    return time_series


if __name__ == "__main__":
	# uvicorn.run(app, host="0.0.0.0", port=8000)
    stock = IEXStock(os.environ.get('IEX_TOKEN'), "TSLA")
    logo = stock.get_logo()
    print(logo)