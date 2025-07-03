from collections import defaultdict

class PaperTrader:
    def __init__(self, balance):
        self.balance = balance
        self.holdings = defaultdict(float)
        self.history = []

    def buy(self, symbol, price, amount):
        cost = price * amount
        if self.balance >= cost:
            self.balance -= cost
            self.holdings[symbol] += amount
            self.history.append(("BUY", symbol, price, amount))

    def sell(self, symbol, price, amount):
        if self.holdings[symbol] >= amount:
            self.holdings[symbol] -= amount
            self.balance += price * amount
            self.history.append(("SELL", symbol, price, amount))

    def net_value(self, prices):
        total = self.balance
        for coin, amount in self.holdings.items():
            total += prices.get(coin, 0) * amount
        return round(total, 2)
