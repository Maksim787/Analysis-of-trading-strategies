from strategy_to_test import *
from testing import *

stock = "SNP"
start_date = "2010-01-01"
end_date = "2020-10-31"

# stock = "XIACY"

test = Testing(stock, start_date, end_date)
test.plot_price()

randStrategy = Random()
test.plot_strategy(randStrategy)

trend = Trend(change_periods=8, from_periods=10, duration=10)
test.plot_strategy(trend)

reverseUp = ReverseUp(change_periods=8, from_periods=10, duration=10)
test.plot_strategy(reverseUp)

deviation = Deviation(prev_periods=15, duration=15)
test.plot_strategy(deviation)

deviationMean = DeviationMean(prev_periods=15)
test.plot_strategy(deviationMean)

movingAverage = MovingAverage(ma_peirod=15, duration=15)
test.plot_strategy(movingAverage)
