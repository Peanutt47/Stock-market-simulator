from bs4 import BeautifulSoup
import requests


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        url = f'https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}'
        page = requests.get(url)
        self.__soup = BeautifulSoup(page.text, 'lxml')
        self.__name = None
        self.__price = None
        self.__price_change = None
        self.__info = None
        if self.have_ticker():
            self.__name = self.__soup.find('h1', class_='D(ib) Fz(18px)').text
            self.__price = float(self.__soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text)
            self.__price_change = float(self.__soup.find('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')["value"])
            self.__info = self.__soup.find("p", class_="businessSummary Mt(10px) Ov(h) Tov(e)").text.split(" ")
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

    def info(self):
        lst2 = []
        for i in range(len(self.__info)):
            if i % 10 == 0:
                lst2.append(" ".join(self.__info[i:i + 10]))
        print("\n".join(lst2))
    # def __str__(self):
    #     return f"{self.name}\n"f"Stock Current Price is: " + f"{self.price:.2f}\n" \
    #            + f"Stock Price Change is: " + f"{self.price_change:.2f}\n" + f"{self.detail}"

# print(ParsePrice())
# while True:
#     print('Stock Current Price is: ' + f"{float(ParsePrice()[0]):.2f}")
#     print('Stock Price Change is: ' + f"{float(ParsePrice()[1]):.2f}")

# x = Stock("BTC-USD")
# print(x.name)
# print(x.price)
# print(x.price_change)
# print(x.detail)
url = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
name = soup.findAll('div', class_="D(ib) Mend(20px)")
print(name)
# print(Stock(input("Enter : ")))
