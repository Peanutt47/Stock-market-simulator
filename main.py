from user import User
from market import Market
from stock_user import UserStock
from stock import Stock
import json
from bs4 import BeautifulSoup
import requests

user_data = User("admin", "12345", 10000)
market = Market("admin",user_data)


def create_account():
    global user_data
    print("Register Menu")
    username = input("Enter your username or (Q)uit: ")
    if username.lower() == "quit" or username.lower() == "q":
        print(f"-"*42+f"\n")
        main()
    elif username == "":
        print("Username cannot be empty!")
        print(f"-"*42+f"\n")
        create_account()
    password = input("Enter your password: ")
    money = input("Enter your money: ")
    if money == "":
        money = 10000
    try:
        with open("user_data.json", "r") as user_flie:
            user_data = json.load(user_flie)
    except FileNotFoundError:
        User(username, password, money).create_account()
        print(f"-"*42+f"\n")
        main()
    else:
        if username in user_data:
            print("Username already exists!")
            print(f"-" * 42 + f"\n")
            create_account()
        else:
            User(username, password, money).create_account()
            print(f"-"*42+f"\n")
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
    print("Login Menu")
    username = input("Enter your username or (Q)uit: ")
    if username.lower() == "quit" or username.lower() == "q":
        print(f"-"*42+f"\n")
        main()
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
                # market = Market(User(username, password, user_data[username]["money"])) #error
                tem = {}
                for i,j in user_data[username]["stocks"].items():
                    tem[i] = UserStock(i,j[i])
                user_data[username]["stocks"] = tem
                market = Market(username,user_data[username])
                print(f"-"*42+f"\n")
                trade_menu()
            else:
                print("Incorrect password!")
                print(f"-"*42+f"\n")
                login()
        elif username not in user_data:
            print("Username does not exist!")
            print(f"-"*42+f"\n")
            login()


def trending_tickers():
    url = "https://finance.yahoo.com/lookup"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.findAll("td", {"class": "data-col0 Ta(start) Pstart(6px) Pend(15px)"})
    price = soup.findAll("td", {"class": "data-col2 Ta(end) Pstart(20px)"})
    change = soup.findAll("td", {"class": "data-col3 Ta(end) Pstart(20px)"})
    percent = soup.findAll("td", {"class": "data-col4 Ta(start) Pstart(20px) Pend(6px) W(130px)"})
    tem = {}
    for i in range(len(name)):
        tem[i + 1] = name[i].text, price[i].text, change[i].text, percent[i].text
    with open("tickers.json", "w") as tickers:
        json.dump(tem, tickers)
    with open("tickers.json", "r") as tickers:
        file = json.load(tickers)

    print(f"-" * 50, end="")
    print(f"-")
    print(f"|{'NO.':^5}|{'Ticker':^10}|{'Price':^10}|{'Change':^10}|{'% Change':^10}|")
    print(f"-" * 50, end="")
    print(f"-")
    for i in range(len(file)):
        print(
            f"|{i + 1:^5}|{file[str(i + 1)][0]:^10}|{file[str(i + 1)][1]:^10}|{file[str(i + 1)][2]:^10}|{file[str(i + 1)][3]:^10}|")
        print(f"-" * 50, end="")
        print(f"-")
    # for i in range(len(x)):
    #     tem[i + 1] = x[i].text
    # with open("tickers.json", "w") as tickers:
    #     json.dump(tem, tickers)
    # with open("tickers.json", "r") as tickers:
    #     tickers = json.load(tickers)
    # # for i in range(len(file)):
    # #     print(f"{i+1}. {file.readline()}")
    # text = []
    # print(f"-" * 48, end="")
    # print(f"-")
    # tem_text = ""
    # r = 1
    # for i in tickers:
    #     if int(i) % 3 == 0:
    #         tem_text += f"| {i}. {tickers[i]}"
    #         if len(tem_text) < 48:
    #             tem_text += " " * (48 - len(tem_text))
    #         tem_text += "|"
    #         text.append(tem_text)
    #         text.append("-------------------------------------------------")
    #         tem_text = ""
    #         r = 1
    #     elif r == 1:
    #         tem_text += f"| {i}. {tickers[i]}"
    #         if len(tem_text) < 16:
    #             tem_text += " " * (16 - len(tem_text))
    #         r += 1
    #     elif r == 2:
    #         tem_text += f"| {i}. {tickers[i]}"
    #         if len(tem_text) < 32:
    #             tem_text += " " * (32 - len(tem_text))
    #         r += 1
    # for i in text:
    #     print(i)


def trade_menu():
    print("Just HODL!!")
    print(f"{market.username} has ${market.user['money']}")
    print("1. Buy Stock")
    print("2. Sell Stock")
    print("3. Trending Tickers")
    print("4. View Portfolio")
    print("5. View Stock info")
    print("6. Logout")
    choice = input("Enter your choice: ")
    if choice == "1":
        ticker = input("Enter the ticker of the stock: ").upper()
        if ticker == "":
            print("Invalid ticker")
            print(f"-"*42+f"\n")
            trade_menu()
        quantity = input("Enter the quantity of the stock: ")
        if quantity.isdigit():
            market.buy(ticker, int(quantity))
            # market.view_portfolio()
        else:
            print("Invalid quantity")
            print(f"-"*42+f"\n")
            trade_menu()
        print(f"-"*42+f"\n")
        trade_menu()
    elif choice == "2":
        ticker = input("Enter the ticker of the stock: ").upper()
        if ticker == "":
            print("Invalid ticker")
            print(f"-"*42+f"\n")
            trade_menu()
        quantity = input("Enter the quantity of the stock: ")
        if quantity.isdigit():
            market.sell(ticker, int(quantity))
        else:
            print("Invalid quantity")
            # market.view_portfolio()
        print(f"-"*42+f"\n")
        trade_menu()
    elif choice == "3":
        print()
        trending_tickers()
        trade_menu()
    elif choice == "4":
        market.view_portfolio()
        print(f"-" * 42 + f"\n")
        trade_menu()
    elif choice == "5":
        ticker = input("Enter the ticker of the stock: ").upper()
        if ticker == "":
            print("Invalid ticker")
            print(f"-"*42+f"\n")
            trade_menu()
        stock = Stock(ticker)
        if stock.have_ticker():
            print(f"Price: {stock.price}")
            print(f"Price Change: {stock.price_change}")
            print(f"Price Change Percentage: {stock.price_change_percent:.4f}%")
            stock.info()
        else:
            print("Invalid ticker")
        print(f"-"*42+f"\n")
        trade_menu()
    elif choice == "6":
        print(f"-"*42+f"\n")
        main()
    else:
        print("Invalid choice")
        print(f"-"*42+f"\n")
        trade_menu()


def main():
    print("Welcome to the Stock Market Simulator!")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        print(f"-"*42+f"\n")
        create_account()
    elif choice == "2":
        print(f"-"*42+f"\n")
        login()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice")
        print(+f"-"*42+f"\n")
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
