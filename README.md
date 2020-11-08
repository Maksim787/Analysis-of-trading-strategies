# Analysis-of-trading-strategies.
With this program you can simply write your own trading strategy and test it on previous market prices.

## Installation
- Download Trading Strategies module
- Install Python 3
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas, matplotlib, yfinance.

```bash
pip install pandas
pip install matplotlib
pip install yfinance
```
 
## Usage
### Testing already written strategy
Open ```main.py``` file

Take any stock and period to analyze. You can find it on [yahoo finance](https://finance.yahoo.com/)
```python
stock = "SNP"
start_date = "2010-01-01"
end_date = "2020-10-31"
```

Instantiate a testing system
```python
test = Testing(stock, start_date, end_date)
```
Plot market prices to verify that it is downloaded correctly
```python
test.plot_price()
```

Instantiate one of the builded strategies and plot it's profit.
```python
randStrategy = Random()
test.plot_strategy(randStrategy)
```

### Writing your own strategy
Open ```strategy_to_test.py``` file

Inherit strategy from ```Strategy``` class. If you want to write your ```__init__``` method, write ```super().__init__()``` in the method firstly:
```python
class YourStrategyName(Strategy):
    def __init__(self):
        super().__init__()
```

Implement two methods: ```make_decision(self)``` (mandatory), ```get_name(self)``` (optional, you can set attribute self.name in ```__init___``` method)

#### make_decision method
You have an access to:
- ```self.price_history``` - list of previous prices
- ```self.curr_price``` - current price at the market
- ```self.orders``` - list of holded orders

Method returns ```None``` (if you don't do anything), ```Order``` object (if you place one order) or list of ```Order``` objects if you place several orders.

Be carefull. You do not need to add orders to ```self.orders```, because when you return an order, testing system do it automatically.

#### Order class:
Creating order object:
```python
order = Order(direction=1, duration=None, take_profit=None,  stop_loss=None)
```
- ```direction``` - an indicator of buying (1) or selling (-1).
- ```duration``` - time from starting date when system close your order immediately.
- ```take_profit``` and ```stop_loss``` - price levels at you want to close orders. For example, you buy at 1000$ price and want to automatically take profit when price reaches take_profit=1100$ and stop your losses when price reaches stop_loss=800$ (order will be closed). With selling orders it works in the same way.

You have access to your previous orders in self.orders attribute in your Strategy class.

Each order have:
- ```days_from_open``` property which returns days from the open.
- close() method which closes your order

You can change ```duration```, ```take_profit``` and ```stop_loss``` attributes. But you have read-only access to ```direction``` attribute.

Example of creating and testing your strategy:
```strategy_to_test.py```:
```python
import random
from random import random as rnd


class NewStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = 'New Strategy'
        random.seed(1)

    def make_decision(self):
        # closing orders
        for order in self.orders:
            if rnd() < 0.1:
                order.close()
        # opening new order
        if rnd() < 0.5:
            return Order(random.choice([-1, 1]))
```
```main.py```:
```python
stock = "SNP"
start_date = "2010-01-01"
end_date = "2020-10-31"

test = Testing(stock, start_date, end_date)
test.plot_price()

newStrategy = NewStrategy()
test.plot_strategy(newStrategy)
```
