import sys

from bs4 import BeautifulSoup
import requests


class Stock:
    def __init__(self, ticker):
        """
        :param ticker: ticker of the stock
        :param soup: HTML soup of the stock
        :param price: price of the stock
        :param price_change: price change of the stock
        :param price_change_percent: price change percent of the stock
        :param info: info of the stock
        """
        self.ticker = ticker  # ticker of the stock
        url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'  # url of the stock
        try:  # try to get the url
            page = requests.get(url)
        except requests.exceptions.ConnectionError:  # if can't connect to network
            print("No internet connection")
            sys.exit()
        self.__soup = BeautifulSoup(page.text, 'lxml')  # save the html to soup
        self.__name = ""  # name of the stock
        self.__price = 0  # price of the stock
        self.__price_change = 0  # price change of the stock
        self.__price_change_percent = 0  # price change percent of the stock
        self.__info = ""  # info of the stock
        if self.have_ticker():  # if the ticker is valid
            self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
            self.__price = float(self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text.replace
                                 (",", ""))
            self.__price_change = float(
                self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
            try:  # try to get the info of the stock
                self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")
            except AttributeError:  # if there is no info
                self.__info = "No company information"
            self.__price_change_percent = float(
                self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])

    def have_ticker(self):
        """
        :return: True if the ticker is valid, False if not
        """
        try:
            self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
        except AttributeError:
            return False
        else:
            self.__price = float(
                self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text.replace(",", ""))
            self.__price_change = float(
                self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
            self.__price_change_percent = \
                self.__soup.findAll('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')[-1]["value"]
            try:
                self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")
            except AttributeError:
                self.__info = "No company information"
            return True

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return float(self.__price)

    @property
    def price_change(self):
        return float(self.__price_change)

    @property
    def price_change_percent(self):
        return float(self.__price_change_percent) * 100

    def info(self):
        lst2 = []
        for i in range(len(self.__info)):
            if i % 10 == 0:
                lst2.append(" ".join(self.__info[i:i + 10]))
        print("\n".join(lst2))
