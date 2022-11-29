import json


class User:
    def __init__(self, username, password, money=10000):
        self.money = money
        self.username = username
        self.password = password
        self.__stocks = {}

    @property
    def money(self):
        return float(self.__money)

    @money.setter
    def money(self, money):
        self.__money = money

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def stocks(self):
        return self.__stocks

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, other):
        if not isinstance(other, str):
            return "password must be string"
        else:
            self.__password = other

    def create_account(self):
        if len(self.__password) >= 8 and not self.__password.isnumeric():
            new_account = {
                self.username: {
                    "password": self.password,
                    "money": self.money,
                    "stocks": self.__stocks
                }
            }
            try:
                with open("user_data.json", "r") as user_flie:
                    user_data = json.load(user_flie)
            except FileNotFoundError:
                with open("user_data.json", "w") as user_flie:
                    json.dump(new_account, user_flie, indent=4)
            else:
                user_data.update(new_account)
                with open("user_data.json", "w") as user_flie:
                    json.dump(user_data, user_flie, indent=4)
        else:
            print("password must be 8 characters or more and not only numbers")