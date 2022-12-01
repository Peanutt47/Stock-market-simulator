from stock import Stock
from user import User
from stock_user import UserStock
import json



class Market:
    def __init__(self,username, user):
        self.username = username
        self.user = user # {money: 10000, stocks: {AAPL: object, MSFT: 2}}

    def buy(self, ticker, quantity=1):
        data_list = []
        ticker_t30 = []
        with open("tickers.json", "r") as file:
            data = json.load(file)
            for i in data:
                data_list.append(data[i])
            for i in data_list:
                ticker_t30.append(i[0])
        print(ticker_t30)
        if ticker in ticker_t30:
            print("top30")
            print(len(ticker_t30))
        else:
            stock = Stock(ticker)
            if stock.have_ticker():
                # if float(self.user.money) < int(stock.price) * int(quantity): #none db
                if float(self.user["money"]) < int(stock.price) * int(quantity):
                    print("You don't have enough money to buy this stock!")
                elif float(self.user["money"]) >= stock.price * int(quantity):
                    self.user["money"] -= (stock.price * quantity)
                    if ticker in self.user["stocks"]:
                        self.user["stocks"][ticker] = UserStock(ticker, self.user["stocks"][ticker].quantity+quantity)
                    else:
                        self.user["stocks"][ticker] = UserStock(ticker, quantity)
                    with open("user_data.json", "r") as user_d:
                        user_data = json.load(user_d)
                    user_data[self.username]["stocks"][ticker] = {self.user["stocks"][ticker].ticker: self.user["stocks"][ticker].quantity}
                    user_data[self.username]["money"] = self.user["money"]
                    with open("user_data.json", "w") as user_d:
                        json.dump(user_data, user_d, indent=4)
                    print("You have bought " + str(quantity) + " of " + ticker)
                    self.view_portfolio()
            else:
                print("No ticker stock found!")

    def sell(self, ticker, quantity=1):
        stock = Stock(ticker)
        if ticker not in self.user["stocks"]:
            print("You don't own this stock!")
        elif ticker in self.user["stocks"]:
            if self.user["stocks"][ticker].quantity - quantity == 0:
                self.user["stocks"].pop(ticker)
                self.user["money"] += stock.price * quantity
                print("You have sold " + str(quantity) + " of " + ticker)
            elif self.user["stocks"][ticker].quantity - quantity > 0:
                self.user["stocks"][ticker].quantity -= quantity
                self.user["money"] += stock.price * quantity
                print("You have sold " + str(quantity) + " of " + ticker)
            elif self.user["stocks"][ticker].quantity - quantity < 0:
                print("You don't have enough of this stock to sell!")
            else:
                print("Error")
            with open("user_data.json", "r") as user_d:
                user_data = json.load(user_d)
            user_data[self.username]["stocks"][ticker] = {
                self.user["stocks"][ticker].ticker: self.user["stocks"][ticker].quantity}
            user_data[self.username]["money"] = self.user["money"]
            with open("user_data.json", "w") as user_d:
                json.dump(user_data, user_d, indent=4)
            self.view_portfolio()

    def view_portfolio(self):
        value = []
        with open("user_data.json", "r") as user_data:
            user_data = json.load(user_data)
        print(f"Money: ${user_data[self.username]['money']:.4f}")
        print("Stocks")
        if User.stocks == {}:
            print("You don't own any stocks!")
        else:
            for key, stock in self.user["stocks"].items():
                value.append(stock.quantity*Stock(key).price)
                print(f"{key}: {stock.quantity}, Price: ${stock.quantity*Stock(key).price:.4f}")
            print(f"Portfolio Value: ${sum(value)+user_data[self.username]['money']:.4f}")
            # print(self.user["stocks"])