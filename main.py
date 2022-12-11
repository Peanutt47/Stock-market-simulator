from user import User
from market import Market
from stock_user import UserStock
from stock import Stock
import json
from bs4 import BeautifulSoup
import requests

user_data = User("admin", "admin1234", 10000)  # create default user_data object
market = Market("admin", user_data)  # create a default market object


def create_account():  # create account function
    global user_data   # global variable
    print("Register Menu")
    username = input("Enter your username or (Q)uit: ")  # input username to register
    if username.lower() == "quit" or username.lower() == "q":  # if user input quit or q, go back to main menu
        print(f"-" * 42 + f"\n")
        main()
    elif username == "":  # if user input nothing, go back to main menu
        print("Username cannot be empty!")
        print(f"-" * 42 + f"\n")
        create_account()
    password = input("Enter your password: ")  # input password to register
    money = input("Enter your money: ")  # input money to register
    if money == "":  # if user input nothing, set money to 10000
        money = 10000
    try:  # try to check user_data
        with open("user_data.json", "r") as user_flie:
            user_data = json.load(user_flie)
    except FileNotFoundError:  # if user_data not found, create a new user_data
        User(username, password, money).create_account()
        print(f"-" * 42 + f"\n")
        main()
    else:  # if user_data found, check if username already exist
        if username in user_data:
            print("Username already exists!")
            print(f"-" * 42 + f"\n")
            create_account()
        else:
            User(username, password, money).create_account()
            print(f"-" * 42 + f"\n")
            main()


def login():  # login function
    global market  # global variable
    print("Login Menu")
    username = input("Enter your username or (Q)uit: ")  # input username to login
    if username.lower() == "quit" or username.lower() == "q":  # if user input quit or q, go back to main menu
        print(f"-" * 42 + f"\n")
        main()
    password = input("Enter your password: ")  # input password to login
    try:  # try to check have user_data or not
        with open("user_data.json", "r") as user_file:
            user_data = json.load(user_file)
    except FileNotFoundError:  # if user_data not found, return to create account
        print("Pls create an account first!")
        create_account()
    else:  # if user_data found, check if username and password correct
        if username in user_data:  # if username correct
            if user_data[username]["password"] == password:  # if password correct
                print("Login successful!")
                tem = {}
                for i, j in user_data[username]["stocks"].items():  # loop to get all stocks from json stored in object
                    tem[i] = UserStock(i, j[i])
                user_data[username]["stocks"] = tem  # save all stocks to user_data in term object
                market = Market(username, user_data[username])  # create market object
                print(f"-" * 42 + f"\n")
                trade_menu()
            else:  # if password incorrect, return to login
                print("Incorrect password!")
                print(f"-" * 42 + f"\n")
                login()
        elif username not in user_data:  # if username incorrect, return to login
            print("Username does not exist!")
            print(f"-" * 42 + f"\n")
            login()


def trending_tickers():  # trending tickers function
    url = "https://finance.yahoo.com/lookup"  # url to get trending tickers
    r = requests.get(url)  # get url
    soup = BeautifulSoup(r.text, "html.parser")  # save all html code to soup
    name = soup.findAll("td", {"class": "data-col0 Ta(start) Pstart(6px) Pend(15px)"})  # find name of trending tickers
    price = soup.findAll("td", {"class": "data-col2 Ta(end) Pstart(20px)"})  # find price of trending tickers
    change = soup.findAll("td", {"class": "data-col3 Ta(end) Pstart(20px)"})  # find change of trending tickers
    percent = soup.findAll("td", {"class": "data-col4 Ta(start) Pstart(20px) Pend(6px) W(130px)"})  # find percent of
    # trending tickers
    tem = {}
    for i in range(len(name)):  # loop to get all trending tickers
        tem[i + 1] = name[i].text, price[i].text, change[i].text, percent[i].text
    with open("tickers.json", "w") as tickers:  # save trending tickers to tickers.json
        json.dump(tem, tickers)
    with open("tickers.json", "r") as tickers:  # read tickers.json
        file = json.load(tickers)
    print(f"-" * 50, end="")
    print(f"-")
    print(f"|{'NO.':^5}|{'Ticker':^10}|{'Price':^10}|{'Change':^10}|{'% Change':^10}|")
    print(f"-" * 50, end="")
    print(f"-")
    for i in range(len(file)):  # loop to print all trending tickers
        print(
            f"|{i + 1:^5}|{file[str(i + 1)][0]:^10}|{file[str(i + 1)][1]:^10}|{file[str(i + 1)][2]:^10}|"
            f"{file[str(i + 1)][3]:^10}|")
        print(f"-" * 50, end="")
        print(f"-")


def trade_menu():  # trade menu function
    print("Just HODL!!")
    print(f"{market.username} has ${market.user['money']}")
    print("1. Buy Stock")
    print("2. Sell Stock")
    print("3. Trending Tickers")
    print("4. View Portfolio")
    print("5. View Stock info")
    print("6. Logout")
    choice = input("Enter your choice: ")  # input choice to trade
    if choice == "1":  # if user input 1, go to buy stock function
        ticker = input("Enter the ticker of the stock: ").upper()  # input ticker(upper) to buy
        if ticker == "":  # if user input nothing, return to trade menu
            print("Invalid ticker")
            print(f"-" * 42 + f"\n")
            trade_menu()
        quantity = input("Enter the quantity of the stock: ")  # input quantity to buy
        if quantity.isdigit():  # if quantity is digit, go to buy stock function
            market.buy(ticker, int(quantity))
        else:  # if quantity is not digit, return to trade menu
            print("Invalid quantity")
            print(f"-" * 42 + f"\n")
            trade_menu()
        print(f"-" * 42 + f"\n")
        trade_menu()
    elif choice == "2":  # if user input 2, go to sell stock function
        ticker = input("Enter the ticker of the stock: ").upper()
        if ticker == "":  # if user input nothing, return to trade menu
            print("Invalid ticker")
            print(f"-" * 42 + f"\n")
            trade_menu()
        quantity = input("Enter the quantity of the stock: ")
        if quantity.isdigit():  # if quantity is digit, go to sell stock function
            market.sell(ticker, int(quantity))
        else:  # if quantity is not digit, return to trade menu
            print("Invalid quantity")
        print(f"-" * 42 + f"\n")
        trade_menu()
    elif choice == "3":  # if user input 3, go to trending tickers function
        print()
        trending_tickers()
        trade_menu()
    elif choice == "4":  # if user input 4, go to view portfolio function
        market.view_portfolio()
        print(f"-" * 42 + f"\n")
        trade_menu()
    elif choice == "5":  # if user input 5, go to view stock info function
        ticker = input("Enter the ticker of the stock: ").upper()
        if ticker == "":  # if user input nothing, return to trade menu
            print("Invalid ticker")
            print(f"-" * 42 + f"\n")
            trade_menu()
        stock = Stock(ticker)
        if stock.have_ticker():  # if ticker is valid, go to view stock info function
            print(f"Price: ${stock.price:.4f}")
            print(f"Price Change: {stock.price_change:.4f}")
            print(f"Price Change Percentage: {stock.price_change_percent:.4f} %")
            stock.info()
        else:  # if ticker is not valid, return to trade menu
            print("Invalid ticker")
        print(f"-" * 42 + f"\n")
        trade_menu()
    elif choice == "6":  # if user input 6, go to main menu function
        print(f"-" * 42 + f"\n")
        main()
    else:  # if user input other than 1-6, return to trade menu
        print("Invalid choice")
        print(f"-" * 42 + f"\n")
        trade_menu()


def main():  # main menu function
    print("Welcome to the Stock Market Simulator!")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")  # input choice to main menu
    if choice == "1":  # if user input 1, go to create account function
        print(f"-" * 42 + f"\n")
        create_account()
    elif choice == "2":  # if user input 2, go to login function
        print(f"-" * 42 + f"\n")
        login()
    elif choice == "3":  # if user input 3, exit the program
        exit()
    else:  # if user input other than 1-3, return to main menu
        print("Invalid choice")
        print(f"-" * 42 + f"\n")
        main()


if __name__ == "__main__":
    main()
