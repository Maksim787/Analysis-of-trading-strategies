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
#### Testing already written strategy
Open main.py file

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

#### Writing your own strategy
Open strategy_to_test.py file

Inherit strategy from Strategy class. If you want to write your __init__ method, write also super().__init__() firstly:
```python
class YourStrategyName(Strategy):
    def __init__(self):
        super().__init__()
```
