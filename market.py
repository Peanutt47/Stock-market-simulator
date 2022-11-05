from stock import Stock
from user import User



class Market:
    def __init__(self, user):
        self.user = user

    def buy(self, ticker, quantity=1):
        stock = Stock(ticker)
        if int(self.user.money) < int(stock.price) * int(quantity):
            print("You don't have enough money to buy this stock!")
        elif self.user.money >= stock.price * int(quantity):
            self.user.money -= (stock.price * quantity)
            self.user.stocks[ticker] = quantity
            print("You have bought " + str(quantity) + " of " + ticker)

    def sell(self, ticker, quantity=1):
        stock = Stock(ticker)
        if ticker not in self.user.stocks:
            print("You don't own this stock!")
        elif ticker in self.user.stocks:
            self.user.money += stock.price * quantity
            if self.user.stocks[ticker] - quantity == 0:
                self.user.stocks.pop(ticker)
            elif self.user.stocks[ticker] - quantity > 0:
                self.user.stocks[ticker] -= quantity
            elif self.user.stocks[ticker] - quantity < 0:
                print("You don't have enough of this stock to sell!")
            else:
                print("Error")
                self.sell(ticker, quantity)
            print("You have sold " + str(quantity) + " of " + ticker)

    def view_portfolio(self):
        print(f"Money: {self.user.money}")
        print("Stocks")
        if User.stocks == {}:
            print("You don't own any stocks!")
        else:
            for ticker, quantity in self.user.stocks.items():
                print(f"{ticker}: {quantity}")