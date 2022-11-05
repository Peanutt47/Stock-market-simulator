class User:
    def __init__(self, username, password, money=10000):
        self.__money = money
        self.__username = username
        self.__password = password
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

