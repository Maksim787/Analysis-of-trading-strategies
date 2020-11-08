class Order:
    def __init__(self, direction=1, duration=None, stop_loss=None, take_profit=None):
        assert abs(direction) == 1
        self.direction = direction
        self.duration = duration
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        self.closed = False
        self.opened_price = None
        self.closed_price = None
        self.opened_date = None
        self.closed_date = None
        self.market = None

    def close(self):
        self.closed = True

    @property
    def days_from_open(self):
        return self.market.curr_date - self.opened_date


class Strategy:
    def __init__(self):
        self.name = "None"
        self.price_history = []
        self.orders = []
        self.curr_price = None

    def make_decision(self):
        pass

    def add_price(self, price):
        self.price_history.append(price)
        self.curr_price = price
