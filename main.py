from user import User
from market import Market
from stock import Stock
import json
from bs4 import BeautifulSoup
import requests

url = "https://finance.yahoo.com/lookup"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
x = soup.findAll("td", {"class": "data-col0 Ta(start) Pstart(6px) Pend(15px)"})
# for i in range(len(x)):
#     print(i + 1, x[i].text)
open("Trending Tickers.txt", "w").write("\n".join([i.text for i in x]))

user_data = User("admin", "12345", 10000)
market = Market(user_data)


def create_account():
    global user_data
    print("Register")
    username = input("Enter your username or (Q)uit: ")
    password = input("Enter your password: ")
    money = input("Enter your money: ")
    if username.lower() == "quit" or username.lower() == "q":
        main()
    try:
        with open("user_data.json", "r") as user_flie:
            user_data = json.load(user_flie)
    except FileNotFoundError:
        User(username, password, money).create_account()
        main()
    else:
        if username in user_data:
            print("Username already exists!")
            create_account()
        else:
            User(username, password, money).create_account()
            print("Account registered!")
            main()
    # if username != user_data.username:
    #     user_data = User(username, password, money)
    # elif username == "Q":
    #     main()
    # elif username == user_data.username:
    #     print("Username already exists")
    #     create_account()
    # print("Account created successfully!")
    # User(username, password, money).create_account()


def login():
    global market
    print("Login")
    username = input("Enter your username or (Q)uit: ")
    password = input("Enter your password: ")
    # if username in user_data.username:
    #     if user_data.password == password:
    #         print("Login successful!")
    #         trade_menu()
    #     else:
    #         print("Incorrect password!")
    #         login()
    # elif username.lower() == "quit" or username.lower() == "q":
    #     main()
    # elif username not in user_data.username:
    #     print("Username does not exist!")
    #     login()
    try:
        with open("user_data.json", "r") as user_file:
            user_data = json.load(user_file)
    except FileNotFoundError:
        print("Pls create an account first!")
        create_account()
    else:
        if username in user_data:
            if user_data[username]["password"] == password:
                print("Login successful!")
                market = Market(user_data[username])
                trade_menu()
            else:
                print("Incorrect password!")
                login()
        elif username.lower() == "quit" or username.lower() == "q":
            main()
        elif username not in user_data:
            print("Username does not exist!")
            login()


def trade_menu():
    print("Just HODL!!")
    print("1. Buy Stock")
    print("2. Sell Stock")
    print("3. Trading stocks")
    print("3. View Portfolio")
    print("4. View Stock info")
    print("5. Logout")
    choice = input("Enter your choice: ")
    if choice == "1":
        ticker = input("Enter the ticker of the stock: ").upper()
        quantity = int(input("Enter the quantity of the stock: "))
        market.buy(ticker, quantity)
        market.view_portfolio()
        trade_menu()
    elif choice == "2":
        ticker = input("Enter the ticker of the stock: ").upper()
        quantity = int(input("Enter the quantity of the stock: "))
        market.sell(ticker, quantity)
        market.view_portfolio()
        trade_menu()
    elif choice == "3":
        market.view_portfolio()
        trade_menu()
    elif choice == "4":
        ticker = input("Enter the ticker of the stock: ").upper()
        stock = Stock(ticker)
        print(f"Price: {stock.price}")
        print(f"Price Change: {stock.price_change}")
        stock.info()
        trade_menu()
    elif choice == "5":
        main()


def main():
    print("Welcome to the Stock Market Simulator!")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        create_account()
    elif choice == "2":
        login()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice")
        main()


main()
# main()
# while True:
#     print("Welcome to the Stock Market Simulator!")
#     print("1. Create Account")
#     print("2. Login")
#     print("3. Exit")
#     choice = input("Enter your choice: ")
#     if choice == "1":
#         print("Creating Account")
#         username = input("Enter your username: ")
#         password = input("Enter your password: ")
#         money = input("Enter your money: ")
#         user_data[username] = User(username, password, money)
#     elif choice == "2":
#         print("Login")
#         username = input("Enter your username: ")
#         password = input("Enter your password: ")
#         while True:
#             print("1. Buy Stock")
#             print("2. Sell Stock")
#             print("3. View Portfolio")
#             print("4. View Stock Market")
#             print("5. Logout")
#             choice = input("Enter your menu: ")
#             if choice == "1":
#                 print("Buy Stock")
#                 ticker = input("Enter the ticker of the stock you want to buy: ")
#                 quantity = input("Enter the quantity of the stock you want to buy: ")
#                 stock = Stock(ticker)
#                 if stock.price * int(quantity) > user_data[0].money:
#                     print("You don't have enough money to buy this stock")
#                 else:
#                     user_data[0].money -= stock.price * int(quantity)
#                     user_data[0].stocks[ticker] = quantity
#                     print("You have successfully bought the stock")
#             elif choice == "2":
#                 print("Sell Stock")
#                 print(User.stocks)
#                 ticker = input("Enter the ticker of the stock you want to sell: ")
#                 quantity = input("Enter the quantity of the stock you want to sell: ")
#                 stock = Stock(ticker)
#                 if ticker not in user_data[0].stocks:
#                     print("You don't own this stock")
#                 elif int(quantity) > user_data[0].stocks[ticker]:
#                     print("You don't have enough of this stock to sell")
#                 else:
#                     user_data[0].money += stock.price * int(quantity)
#                     user_data[0].stocks[ticker] -= int(quantity)
#                     print("You have sold " + quantity + " of " + ticker)
#             elif choice == "3":
#                 print("View Portfolio")
#                 print(f"Money: {user_data[0].money}")
#                 print("Stocks:")
#                 for ticker, quantity in user_data[0].stocks.items():
#                     print(f"{ticker}: {quantity}")
#             elif choice == "4":
#                 print("View Stock Info")
#                 ticker = input("Enter the ticker of the stock you want to view: ")
#                 print(Stock(ticker))
#             elif choice == "5":
#                 print("Logout")
#                 break
#     elif choice == "3":
#         print(f"GOODLUCK Trader!!!")
#         break
#     else:
#         print("Invalid Choice")
