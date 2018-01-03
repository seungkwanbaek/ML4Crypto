"""
StrategyLearner using Random Forest Classifier Learner

Seungkwan Bryan Baek
sbaek47
"""
import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random

from marketsimcode import compute_portvals

import RTLearner as rl
import BagLearner as bl

class StrategyLearner(object):

    def compute_daily_returns(self, df, day, symbol):
        """Compute and return the daily return values."""
        daily_ret = df.copy()
        daily_ret[:-day] =  (daily_ret[day:].values/daily_ret[: -day].values)-1
        daily_ret.ix[-day:] = 0
        return daily_ret[symbol]

    # constructor
    def __init__(self, verbose = False, impact = 0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = bl.BagLearner(learner = rl.RTLearner, kwargs={"leaf_size":5}, bags = 20, boost = False, verbose=False)

    def build_data(self, symbol, sd, ed, sv):
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY

        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose:
            print prices

        lookback = 14

        norm_prices = prices.divide(prices.ix[0])
        daily_rets = self.compute_daily_returns(norm_prices, lookback, symbol)

        #Calculate the indicators
        rolling_mean = pd.rolling_mean(norm_prices, window = lookback, min_periods = lookback)
        rolling_std = pd.rolling_std(norm_prices, window = lookback, min_periods = lookback)
        up = (rolling_std * 2) + rolling_mean
        down = (rolling_std * -2) + rolling_mean

        df = norm_prices.copy()
        df['bbp']  = (norm_prices - down) / (up - down)
        df['Price/SMA'] = norm_prices/rolling_mean
        df['bollinger_up'] = (rolling_std * 2) + rolling_mean
        df['bollinger_down'] = (rolling_std * -2) + rolling_mean
        df['Price/EMA'] = norm_prices / pd.ewma(norm_prices, span = lookback, min_periods = lookback)
        df = df.drop(symbol, 1)

        YBUY = 0.01
        YSELL = 0

        df['action'] = 0
        df.loc[daily_rets > (YBUY + self.impact), 'action'] = 1
        df.loc[daily_rets < (YSELL + self.impact), 'action'] = -1

        df = df.fillna(value=0).copy()

        data = df.as_matrix()
        X = data[:, :-1]
        Y = data[:, -1].astype(dtype=int)

        return X, Y

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "JPM", \
        sd = dt.datetime(2008,1,1), \
        ed = dt.datetime(2009,12,31), \
        sv = 100000):

        X, Y = self.build_data(symbol, sd, ed, sv)
        self.learner.addEvidence(X, Y)

    def testPolicy(self, symbol = "JPM", \
        sd = dt.datetime(2010,1,1), \
        ed = dt.datetime(2011,12,31), \
        sv = 100000):

        X, Y = self.build_data(symbol, sd, ed, sv)
        answer = self.learner.query(X)

        dates = pd.date_range(sd, ed)

        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols

        YBUY = 0.01
        YSELL = 0

        trades.values[:,:] = 0 # set them all to nothing

        trades.values[answer > (YBUY + 2 * self.impact)] = 1000
        trades.values[answer < (YSELL - 2 * self.impact)] = -1000

        orders = trades.copy()
        orders = orders.diff()

        orders[symbol][0] = trades[symbol][0]

        if self.verbose: print type(orders) # it better be a DataFrame!
        if self.verbose: print orders
        if self.verbose: print prices_all

        return orders

def test():
    learner = StrategyLearner(verbose = False) # constructor
    learner.addEvidence() # training step
    learner.testPolicy() # testing step

if __name__=="__main__":
    test()
