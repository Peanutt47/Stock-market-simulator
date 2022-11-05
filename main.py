from user import User
from stock import Stock
from market import Market

user_data = {}
while True:
    print("Welcome to the Stock Market Simulator!")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("Creating Account")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        money = input("Enter your money: ")
        user_data[username] = User(username, password, money)
    elif choice == "2":
        print("Login")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        while True:
            print("1. Buy Stock")
            print("2. Sell Stock")
            print("3. View Portfolio")
            print("4. View Stock Market")
            print("5. Logout")
            choice = input("Enter your menu: ")
            if choice == "1":
                print("Buy Stock")
                ticker = input("Enter the ticker of the stock you want to buy: ")
                quantity = input("Enter the quantity of the stock you want to buy: ")
                stock = Stock(ticker)
                if stock.price * int(quantity) > user_data[0].money:
                    print("You don't have enough money to buy this stock")
                else:
                    user_data[0].money -= stock.price * int(quantity)
                    user_data[0].stocks[ticker] = quantity
                    print("You have successfully bought the stock")
            elif choice == "2":
                print("Sell Stock")
                print(User.stocks)
                ticker = input("Enter the ticker of the stock you want to sell: ")
                quantity = input("Enter the quantity of the stock you want to sell: ")
                stock = Stock(ticker)
                if ticker not in user_data[0].stocks:
                    print("You don't own this stock")
                elif int(quantity) > user_data[0].stocks[ticker]:
                    print("You don't have enough of this stock to sell")
                else:
                    user_data[0].money += stock.price * int(quantity)
                    user_data[0].stocks[ticker] -= int(quantity)
                    print("You have sold " + quantity + " of " + ticker)
            elif choice == "3":
                print("View Portfolio")
                print(f"Money: {user_data[0].money}")
                print("Stocks:")
                for ticker, quantity in user_data[0].stocks.items():
                    print(f"{ticker}: {quantity}")
            elif choice == "4":
                print("View Stock Info")
                ticker = input("Enter the ticker of the stock you want to view: ")
                print(Stock(ticker))
            elif choice == "5":
                print("Logout")
                break
    elif choice == "3":
        print(f"GOODLUCK Trader!!!")
        break
