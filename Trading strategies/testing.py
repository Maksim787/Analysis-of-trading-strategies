import yfinance as yf
import matplotlib.pyplot as plt
from strategy_class import *
import numpy as np


class Capital:
    def __init__(self, capital=None):
        if capital is None:
            capital = []
        self.capital = capital

    def __iadd__(self, val):
        if self.capital:
            self.capital.append(self.capital[-1] + val)
        else:
            self.capital.append(val)
        return self

    def get_capital(self):
        return np.array(self.capital)


class Testing:
    def __init__(self, stock, start_date, end_date):
        plt.style.use('seaborn')

        self.data = yf.download(stock, start_date, end_date)
        self.price = self.data['Adj Close']
        self.curr_price = self.price[0]
        self.curr_date = 0
        self.capital = None

    def get_dates(self):
        return self.data.index

    def print_data(self):
        print(self.data)

    def print_price(self):
        print(self.price)

    def plot_price(self):
        plt.plot(self.price)
        plt.fill_between(self.price.index, self.price, alpha=0.25)
        plt.title("Price")
        plt.show()

    def plot_strategy(self, strategy):
        capital = self.test_strategy(strategy)
        plt.plot(self.get_dates(), capital)
        plt.fill_between(self.get_dates(),
                         capital, 0, where=(capital > 0),
                         color='green', alpha=0.25, interpolate=True)
        plt.fill_between(self.get_dates(),
                         capital, 0, where=(capital < 0),
                         color='red', alpha=0.25, interpolate=True)
        plt.title(strategy.get_name())
        plt.xlabel("Time")
        plt.ylabel("Yield in %")
        plt.show()

    def test_strategy(self, strategy):
        period = len(self.price)
        self.__completed_orders = []

        # take orders
        for i in range(period):
            self.curr_price = self.price[i]
            self.curr_date = i

            strategy.add_price(self.curr_price)
            self.__take_orders(strategy)
            self.__complete_orders(strategy)

        # complete all orders
        for order in strategy.orders:
            order.close()
        self.__complete_orders(strategy)

        # count capital
        capital = self.__count_capital()
        return capital

    def __add_order(self, new_order, strategy):
        new_order.opened_price = self.curr_price
        new_order.opened_date = self.curr_date
        new_order.market = self
        strategy.orders.append(new_order)

    def __take_orders(self, strategy):
        new_order = strategy.make_decision()
        if new_order is not None:
            if isinstance(new_order, Order):
                self.__add_order(new_order, strategy)
            else:
                for order in new_order:
                    self.__add_order(order, strategy)

    def __complete_orders(self, strategy):
        for order in strategy.orders:
            to_close = order.closed
            if order.duration is not None:
                to_close = to_close or order.duration <= self.curr_date - order.opened_date
            if order.take_profit is not None:
                to_close = to_close or order.take_profit * order.direction < self.curr_price * order.direction
            if order.stop_loss is not None:
                to_close = to_close or order.stop_loss * order.direction > self.curr_price * order.direction

            if to_close:
                strategy.orders.remove(order)
                order.closed_price = self.curr_price
                order.closed_date = self.curr_date
                self.__completed_orders.append(order)

    def __count_capital(self):
        capital = Capital()
        curr_date = 0
        i = 0
        while i < len(self.__completed_orders):
            order = self.__completed_orders[i]
            while curr_date < order.closed_date:
                capital += 0
                curr_date += 1
                order = self.__completed_orders[i]
            change = 0
            while curr_date == order.closed_date:
                change += order.direction * (order.closed_price - order.opened_price) / order.opened_price
                i += 1
                if i == len(self.__completed_orders):
                    break
                order = self.__completed_orders[i]
            capital += change
            curr_date += 1
        while curr_date < len(self.price):
            capital += 0
            curr_date += 1
        return capital.get_capital()
