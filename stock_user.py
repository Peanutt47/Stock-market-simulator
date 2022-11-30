class UserStock:
    def __init__(self, ticker, quantity):
        self.ticker = ticker
        self.quantity = quantity

    @property
    def ticker(self):
        return self.__ticker

    @ticker.setter
    def ticker(self, ticker):
        self.__ticker = ticker

    @property
    def quantity(self):
        return int(self.__quantity)

    @quantity.setter
    def quantity(self, quantity):
        self.__quantity = quantity
