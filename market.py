from stock import Stock
from user import User
from stock_user import UserStock
import json


class Market:
    def __init__(self, username, user):
        """
        :param username: username of the user
        :param user: user object use to store stock object in stocks dictionary
        """
        self.username = username
        self.user = user  # {money: 10000, stocks: {AAPL: 1, MSFT: 2}}

    def buy(self, ticker, quantity=1):
        """
        :param ticker: ticker of the stock
        :param quantity: quantity of the stock
        this method will buy the stock and add it to the user's portfolio
        """
        stock = Stock(ticker)
        if stock.have_ticker():  # check if the stock is valid
            if float(self.user["money"]) < int(stock.price) * int(quantity):  # check if the user has enough money
                print("You don't have enough money to buy this stock!")
            elif float(self.user["money"]) >= stock.price * int(quantity):  # if the user has enough money
                self.user["money"] -= (stock.price * quantity)  # subtract the price of the stock from the user's money
                if ticker in self.user["stocks"]:  # if the user already owns the stock
                    self.user["stocks"][ticker] = UserStock(ticker, self.user["stocks"][ticker].quantity + quantity)
                    # add the quantity to the user's stock
                else:  # if the user doesn't own the stock
                    self.user["stocks"][ticker] = UserStock(ticker, quantity)  # add the stock to the user's portfolio
                with open("user_data.json", "r") as user_d:  # open the user data file
                    user_data = json.load(user_d)
                user_data[self.username]["stocks"][ticker] = {
                    self.user["stocks"][ticker].ticker: self.user["stocks"][ticker].quantity}
                # add the stock to the user data file
                user_data[self.username]["money"] = self.user["money"]  # add the user's money to the user data file
                with open("user_data.json", "w") as user_d:  # open the user data file
                    json.dump(user_data, user_d, indent=4)
                print("You have bought " + str(quantity) + " of " + ticker)
                self.view_portfolio()
        else:  # if the stock is invalid
            print("No ticker stock found!")

    def sell(self, ticker, quantity=1):  # sell the stock
        stock = Stock(ticker)  # create a stock object
        if ticker not in self.user["stocks"]:  # check if the user owns the stock
            print("You don't own this stock!")
        elif ticker in self.user["stocks"]:  # if the user owns the stock
            if self.user["stocks"][ticker].quantity - quantity == 0:  # if the user wants to sell all of the stock
                self.user["stocks"].pop(ticker)  # remove the stock from the user's portfolio
                self.user["money"] += stock.price * quantity  # add the price of the stock to the user's money
                print("You have sold " + str(quantity) + " of " + ticker)
            elif self.user["stocks"][ticker].quantity - quantity > 0:  # if the user wants to sell some of the stock
                self.user["stocks"][ticker].quantity -= quantity  # subtract the quantity from the user's stock
                self.user["money"] += stock.price * quantity  # add the price of the stock to the user's money
                print("You have sold " + str(quantity) + " of " + ticker)
            elif self.user["stocks"][ticker].quantity - quantity < 0:  # if the user wants to sell more than they own
                print("You don't have enough of this stock to sell!")
            else:  # if got bug
                raise Exception("Error")
            with open("user_data.json", "r") as user_d:
                user_data = json.load(user_d)
            user_data[self.username]["stocks"][ticker] = {
                self.user["stocks"][ticker].ticker: self.user["stocks"][ticker].quantity}
            # add the stock to the user data file
            user_data[self.username]["money"] = self.user["money"]  # add the user's money to the user data file
            with open("user_data.json", "w") as user_d:
                json.dump(user_data, user_d, indent=4)
            self.view_portfolio()

    def view_portfolio(self):  # view the user's portfolio
        value = []  # list to store the value of the stocks
        with open("user_data.json", "r") as user_data:
            user_data = json.load(user_data)
        print(f"Money: ${user_data[self.username]['money']:.4f}")
        print("Stocks")
        if User.stocks == {}:  # if the user doesn't own any stocks
            print("You don't own any stocks!")
        else:  # if the user owns stocks
            for key, stock in self.user["stocks"].items():  # loop through the user's stocks
                value.append(stock.quantity * Stock(key).price)
                print(f"{key}: {stock.quantity}, Price: ${stock.quantity * Stock(key).price:.4f}")
            print(f"Portfolio Value: ${sum(value) + user_data[self.username]['money']:.4f}")
