import json
from datetime import datetime, timedelta
import requests


def get_currency_exchange_rates(currency):
    base = "USD"  # reference currency
    start_date = str(datetime.now() - timedelta(1))[:11]  # yesterday
    end_date = str(datetime.today())[:11]  # today
    url = 'https://api.exchangerate.host/timeseries?base={0}&start_date={1}&end_date={2}&symbols={3}'.format(base, start_date, end_date, currency)
    response = requests.get(url)
    data = response.json()

    yesterday, today = "", ""
    if currency == "JPY":
        yesterday = str(data["rates"])[23:33]
        today = str(data["rates"])[58:68]
        # print(yesterday)
        # print(today)
    else:
        yesterday = str(data["rates"])[23:30]
        today = str(data["rates"])[56:64]
        # print(yesterday)  # yesterday
        # print(today)  # today

    data_set = {'currency': currency, 'yesterday': yesterday, 'today': today}
    print(data_set)
    return data_set