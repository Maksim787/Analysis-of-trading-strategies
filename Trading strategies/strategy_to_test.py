from strategy_class import *
import random
from random import random as rnd
from math import sqrt


class Random(Strategy):
    def __init__(self):
        super().__init__()
        self.name = 'Random Strategy'
        random.seed(1)

    def make_decision(self):
        # closing orders
        for order in self.orders:
            if rnd() < 0.1:
                order.close()
        # opening new order
        if rnd() < 0.5:
            return Order(random.choice([-1, 1]))


class Trend(Strategy):
    def __init__(self, change_periods=8, from_periods=10, duration=15):
        super().__init__()
        self.name = 'Trend Strategy'
        self.change_periods = change_periods
        self.from_periods = from_periods
        self.duration = duration

    def count_up_periods(self):
        last = self.price_history[-self.from_periods - 1:]
        up_periods = 0
        for i in range(self.from_periods):
            if last[i] < last[i + 1]:
                up_periods += 1
        return up_periods

    def compare_up_periods(self, up_periods):
        if up_periods >= self.change_periods:
            return Order(1, duration=self.duration)
        elif up_periods <= self.from_periods - self.change_periods:
            return Order(-1, duration=self.duration)

    def make_decision(self):
        if len(self.price_history) >= self.from_periods + 1 and len(self.orders) == 0:
            up_periods = self.count_up_periods()
            return self.compare_up_periods(up_periods)


class ReverseUp(Trend):
    def __init__(self, change_periods=8, from_periods=10, duration=15):
        super().__init__(change_periods, from_periods, duration)
        self.name = 'ReverseUp Strategy'

    def compare_up_periods(self, up_periods):
        if up_periods <= self.from_periods - self.change_periods:
            return Order(1, duration=self.duration)


class Deviation(Strategy):
    def __init__(self, prev_periods=10, duration=15):
        super().__init__()
        self.name = 'Deviation Strategy'
        self.duration = duration
        self.prev_periods = prev_periods

    def find_deviation_mean(self):
        n = self.prev_periods
        x_sum = 0
        x_2_sum = 0
        for i in self.price_history[-n:]:
            x_sum += i
            x_2_sum += i * i
        mean = x_sum / n
        dev = sqrt((x_2_sum - 2 * x_sum * mean + mean * mean * n) / (n - 1))
        return dev, mean

    def make_decision(self):
        if len(self.price_history) >= self.prev_periods:
            dev, mean = self.find_deviation_mean()
            order = None
            if self.curr_price > mean + dev:
                order = Order(-1, self.duration)
            if self.curr_price < mean - dev:
                order = Order(1, self.duration)
            return order


class DeviationMean(Deviation):
    def __init__(self, prev_periods=15):
        super().__init__(prev_periods)
        self.name = 'Deviation/Mean Strategy'

    def close(self):
        dev, mean = self.find_deviation_mean()
        closeVal = 1 if self.curr_price > mean else -1
        for order in self.orders:
            if order.direction == closeVal:
                order.close()

    def make_decision(self):
        self.close()
        order = super().make_decision()
        if order is not None:
            order.duration = None
        return order


class MovingAverage(Strategy):
    def __init__(self, ma_peirod=15, duration=15):
        super().__init__()
        self.name = 'Moving Average Strategy'
        self.duration = duration
        self.ma_period = ma_peirod

    def make_decision(self):
        if len(self.price_history) >= self.ma_period:
            ma_val = sum(self.price_history[-self.ma_period:]) / self.ma_period
            if ma_val >= self.curr_price:
                return Order(1, self.duration)
            else:
                return Order(-1, self.duration)
