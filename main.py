from bs4 import BeautifulSoup
import requests


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        url = f'https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}'
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'lxml')
        self.name = self.soup.find('h1', class_='D(ib) Fz(18px)').text
        self.price = float(self.soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text)
        self.price_change = float(self.soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])



    def __str__(self):
        return f"{self.name}\n"f"Stock Current Price is: " + f"{self.price:.2f}\n" + f"Stock Price Change is: " + f"{self.price_change:.2f}"

# print(ParsePrice())
# while True:
#     print('Stock Current Price is: ' + f"{float(ParsePrice()[0]):.2f}")
#     print('Stock Price Change is: ' + f"{float(ParsePrice()[1]):.2f}")

print(Stock("AAPL"))
# url = 'https://finance.yahoo.com/quote/AAPL?p=AAPL'
# page = requests.get(url)
# soup = BeautifulSoup(page.text, 'lxml')
# name = soup.find('h1', class_='D(ib) Fz(18px)').text
# print(name)