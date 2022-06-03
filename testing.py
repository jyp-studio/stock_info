#%%
# backtest and strategy
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

# %%
# original test
class SmaCross(Strategy):
    # class variables
    n1 = 5
    n2 = 20

    def init(self):
        price = self.data.Close
        # define moving average and
        # use function of SMA in backtesting.py to plot it
        self.ma1 = self.I(SMA, price, self.n1)
        self.ma2 = self.I(SMA, price, self.n2)

    def next(self):
        """
        if ma1 > ma2 means the stock is getting great => buy it
        elif ma1 < ma2 means the stock is getting worse => sell it
        """
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


# %%
