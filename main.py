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
import datetime
import json
import pandas
import random
from urllib.parse import urlencode
from urllib.request import urlopen

import redis
from fastapi import FastAPI
import yahoo_fin.stock_info as si

import os

from currency import *
from iex_service import IEXStock

app = FastAPI()
redis_client = redis.Redis(host='alek-redis.apps.okd4.csh.rit.edu', port=443, db=0)


@app.get("/logo/{ticker}")
def read_logo(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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
        print(logo)

    return logo


@app.get("/company-info/{ticker}")
def read_company_info(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return company_info


@app.get("/stats/{ticker}")
def read_stats(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return stats


# Can also handle a request for any amount of news posts
@app.get("/news/{ticker}")
def read_news(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return news


# Can also specify range (in years) of news to gather
@app.get("/dividends/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return dividends


@app.get("/institutional-ownership/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return institutional_ownership


@app.get("/insider-transactions/{ticker}")
def read_dividends(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
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

    return insider_transactions


@app.get("/ceo-compensation/{ticker}")
def read_ceo_compensation(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
    ceo_compensation_info_key = f"{ticker}_ceo-compensations"
    ceo_compensation = redis_client.get(ceo_compensation_info_key)

    if ceo_compensation is None:
        print("Retrieving data from API...")
        ceo_compensation = stock.get_ceo_compensation()
        redis_client.set(ceo_compensation_info_key, json.dumps(ceo_compensation))
        redis_client.expire(ceo_compensation_info_key, datetime.timedelta(days=7))
    else:
        print("Retrieving data from cache...")
        ceo_compensation = json.loads(ceo_compensation)

    return ceo_compensation


# @app.get("/today-earnings/")
# def read_today_earnings():
#     stock = IEXStock(os.enviorn.get('IEX_TOKEN'), None)
#     today_earnings_info_key = "today-earnings"
#     today_earnings = redis_client.get(today_earnings_info_key)
#
#     if today_earnings is None:
#         print("Retrieving data from API...")
#         today_earnings = stock.get_today_earnings()
#         redis_client.set(today_earnings_info_key, json.dumps(today_earnings))
#         redis_client.expire(today_earnings_info_key, datetime.timedelta(days=1))
#     else:
#         print("Retrieving data from cache...")
#         today_earnings = json.loads(today_earnings)
#
#     return today_earnings


@app.get("/dividends-forcast/{ticker}")
def read_dividends_forcast(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
    dividends_forcast_info_key = f"{ticker}_dividends-forcast"
    dividends_forcast = redis_client.get(dividends_forcast_info_key)

    if dividends_forcast is None:
        print("Retrieving data from API...")
        dividends_forcast = stock.get_dividends_forcast()
        redis_client.set(dividends_forcast_info_key, json.dumps(dividends_forcast))
        redis_client.expire(dividends_forcast_info_key, datetime.timedelta(days=7))
    else:
        print("Retrieving data from cache...")
        dividends_forcast = json.loads(dividends_forcast)

    return dividends_forcast


@app.get("/analyst-ratings/{ticker}")
def read_analyst_ratings(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
    analyst_ratings_info_key = f"{ticker}_analyst-ratings"
    analyst_ratings = redis_client.get(analyst_ratings_info_key)

    if analyst_ratings is None:
        print("Retrieving data from API...")
        analyst_ratings = stock.get_analyst_ratings()
        redis_client.set(analyst_ratings_info_key, json.dumps(analyst_ratings))
        redis_client.expire(analyst_ratings_info_key, datetime.timedelta(days=7))
    else:
        print("Retrieving data from cache...")
        analyst_ratings = json.loads(analyst_ratings)

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
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), "")
    sector_key = "sector"
    sectors = redis_client.get(sector_key)

    if sectors is None:
        print("Retrieving data from API...")
        sectors = stock.get_sector_data()
        redis_client.set(sector_key, json.dumps(sectors))
        redis_client.expire(sector_key, datetime.timedelta(days=1))
    else:
        print("Retrieving data from cache...")
        sectors = json.loads(sectors)

    return sectors


@app.get('/currency')
def get_currency_rates():
    return [get_currency_exchange_rates("EUR"), get_currency_exchange_rates("JPY"),
            get_currency_exchange_rates("GBP"), get_currency_exchange_rates("AUD"),
            get_currency_exchange_rates("CAD"), get_currency_exchange_rates("CNY")]


@app.get('/analyst/{ticker}')
def get_analyst_ratings(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), "")
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

    return data['quoteSummary']['result']


@app.get('/dividends-history/{ticker}')
def get_dividends_forcast(ticker: str):
    analysts = si.get_analysts_info(ticker)['Earnings History']
    return json.loads(analysts.to_json())


@app.get("/time-series-1d/{ticker}")
def read_dividends_forcast(ticker: str):
    stock = IEXStock(os.enviorn.get('IEX_TOKEN'), ticker)
    time_series = stock.get_time_series_data()

    return time_series
