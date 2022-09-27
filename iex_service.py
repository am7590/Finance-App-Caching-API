import requests


class IEXStock:

    def __init__(self, token, symbol):
        self.BASE_URL = 'https://cloud.iexapis.com/stable'

        self.token = token
        self.symbol = symbol

    def get_logo(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_company_info(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r = requests.get(url)
        response = r.json()
        # st.write(response)
        return response

    def get_stats(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_company_news(self, last=20):
        url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_dividends(self, range='5y'):
        url = f"{self.BASE_URL}/stock/{self.symbol}/dividends/{range}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_institutional_ownership(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_insider_transactions(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/insider-transactions?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_ceo_compensation(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/ceo-compensation?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_today_earnings(self):
        url = f"{self.BASE_URL}/stock/market/today-earnings?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_dividends_forcast(self):
        url = f"{self.BASE_URL}/time-series/DIVIDENDS_FORECAST/{self.symbol}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_analyst_ratings(self):
        url = f"{self.BASE_URL}/time-series/CORE_ESTIMATES/{self.symbol}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_sector_data(self):
        url = f"{self.BASE_URL}/stock/market/sector-performance/?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_time_series_data(self):
        # https://cloud.iexapis.com/stable/stock/{self.symbol}/chart/1d?token=pk_b8d39299974f41f99ef8f79101ab2617
        url = f"{self.BASE_URL}/stock/{self.symbol}/chart/1d?token={self.token}"
        r = requests.get(url)

        return r.json()