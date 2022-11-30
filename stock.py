import sys

from bs4 import BeautifulSoup
import requests


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("No internet connection")
            sys.exit()
        self.__soup = BeautifulSoup(page.text, 'lxml')
        self.__name = ""
        self.__price = 0
        self.__price_change = 0
        self.__price_change_percent = 0
        self.__info = ""
        if self.have_ticker():
            self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
            self.__price = float(self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text)
            self.__price_change = float(self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
            self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")
            self.__price_change_percent = float(self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
        # self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
        # self.__price = float(self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text)
        # self.__price_change = float(self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
        # self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")

    def have_ticker(self):
        try:
            self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
        except AttributeError:
            return False
        else:
            self.__price = float(self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text)
            self.__price_change = float(
                self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
            self.__price_change_percent = self.__soup.findAll('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')[-1]["value"]
            self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")
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
        return float(self.__price_change_percent)*100
        # return self.__price_change_percent
    def info(self):
        lst2 = []
        for i in range(len(self.__info)):
            if i % 10 == 0:
                lst2.append(" ".join(self.__info[i:i + 10]))
        print("\n".join(lst2))
    # def __str__(self):
    #     return f"{self.name}\n"f"Stock Current Price is: " + f"{self.price:.2f}\n" \
    #            + f"Stock Price Change is: " + f"{self.price_change:.2f}\n" + f"{self.detail}"


# import time
#
# from settrade_v2 import Investor
#
# investor = Investor(
#                 app_id="9HCH2mlwPzy81nSz",
#                 app_secret="AOvWCOarao7STFT+Acfr0EnCNHo9hAC2Xd8US+s/e1Dc",
#                 broker_id="SANDBOX",
#                 app_code="SANDBOX",
#                 is_auto_queue=False)
# realtime = investor.RealtimeDataConnection()
#
# def my_message(result):
#     print(result)
#
# sub = realtime.subscribe_price_info("AOT", on_message = my_message)
# sub.start()
# # run main thread forever
# while True:
#     time.sleep(1)
# print("End")
# print(Stock("TSLA").price_change)
