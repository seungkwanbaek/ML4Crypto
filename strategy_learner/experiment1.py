"""
Compare StrategyLearner with manual_strategy and benchmark

Seungkwan Bryan Baek
sbaek47
"""

import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random
import matplotlib.pyplot as plt

import RTLearner as rl
import BagLearner as bl
import StrategyLearner as sl
import ManualStrategy as ms

def author():
    return 'sbaek47'

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns=df.copy()
    daily_returns[1:]=(daily_returns[1:]/daily_returns[:-1].values)-1
    daily_returns.ix[0] = 0
    return daily_returns

def stat_summary(df):

    norm_df = df.divide(df.ix[0])

    daily_rets = compute_daily_returns(norm_df)
    daily_rets = daily_rets[1:]
    #Cumulative return
    cr = (norm_df[-1]/norm_df[0])-1

    #Average Daily Return
    adr=daily_rets.mean()

    #Std dev of daily return
    sddr=daily_rets.std()

    #Sharpe Ratio
    sr=np.sqrt(252.0)*(adr-0)/(sddr)

    return cr, adr, sddr, sr

###############################################################

sv = 100000
sd_train = dt.datetime(2008,01,01)
ed_train = dt.datetime(2009,12,31)

# sd_test = dt.datetime(2010,01,01)
# ed_test = dt.datetime(2011,12,31)

sym = "JPM"

#Strategy Learner
learner = sl.StrategyLearner(verbose = False)
learner.addEvidence(symbol = sym, sd = sd_train, ed = ed_train, sv = sv)
orders_Strategy = learner.testPolicy(symbol = sym, sd = sd_train, \
    ed = ed_train, sv = sv)

#Manual Strategy
orders_Manual = ms.testPolicy(symbol = sym, sd = sd_train, \
    ed = ed_train, sv = sv)

#Manual Strategy Portfolio Value
df_Manual = ms.compute_portvals(orders_Manual, start_val = sv, commission = 0, impact = 0)

#benchmark
orders_benchmark = ms.testPolicy_benchmark(symbol = sym, sd = sd_train, \
    ed = ed_train, sv = sv)

#Manual Strategy Portfolio Value
df_benchmark = ms.compute_portvals(orders_benchmark, start_val = sv, commission = 0, impact = 0)

################################################################

#Strategy Learner Portfolio Value
dates = pd.date_range(sd_train, ed_train)
prices = ut.get_data([sym], dates, False)
prices = prices.assign(Cash = 1.0)

prices = prices.dropna(axis=0)
impact = 0

orders_Strategy = orders_Strategy.assign(Cash = 0)

for i in range(len(orders_Strategy)):
    if (orders_Strategy[sym][i] > 0):
        orders_Strategy['Cash'][i] += (1 + impact) * (prices[sym][i] * - orders_Strategy[sym][i])
    else:
        orders_Strategy['Cash'][i] += (1 - impact) * (prices[sym][i] * - orders_Strategy[sym][i])


for j in range(len(orders_Strategy.columns)):
        stock = 0
        for i in range(len(orders_Strategy)):
            orders_Strategy.iloc[i,j] = stock + orders_Strategy.iloc[i,j]
            stock = orders_Strategy.iloc[i,j]

orders_Strategy['Cash'] = orders_Strategy['Cash'] + sv

value = orders_Strategy * prices
df_Strategy = value.sum(axis=1)

###############################################################################

benchmark_cr, benchmark_adr, benchmark_sddr, benchmark_sr = ms.stat_summary(df_benchmark)

manual_cr, manual_adr, manual_sddr, manual_sr = ms.stat_summary(df_Manual)

Strategy_cr, Strategy_adr, Strategy_sddr, Strategy_sr = ms.stat_summary(df_Strategy)

print "Cumulative Return of Benchmark: {}".format(benchmark_cr)
print "Cumulative Return of Manual: {}".format(manual_cr)
print "Cumulative Return of Strategy: {}".format(Strategy_cr)
print
print "Standard Deviation of Benchmark: {}".format(benchmark_adr)
print "Standard Deviation of Manual: {}".format(manual_adr)
print "Standard Deviation of Strategy: {}".format(Strategy_adr)
print
print "Average Daily Return of Benchmark: {}".format(benchmark_sddr)
print "Average Daily Return of Manual: {}".format(manual_sddr)
print "Average Daily Return of Strategy: {}".format(Strategy_sddr)
print
print "SR of Benchmark: {}".format(benchmark_sr)
print "SR of Manual: {}".format(manual_sr)
print "SR of Strategy: {}".format(Strategy_sr)
print
print "Final Portfolio Value of Benchmark: {}".format(df_benchmark[-1])
print "Final Portfolio Value of Manual: {}".format(df_Manual[-1])
print "Final Portfolio Value of Strategy: {}".format(df_Strategy[-1])
###############################################################################
ax = df_Strategy.plot(title = "Strategy vs. Manual vs. Benchmark", fontsize = 12, color = "Black")
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value")
df_Manual.plot(ax=ax, color="Blue")
df_benchmark.plot(ax=ax, color="Green")

ax.legend(["Strategy", "Manual", "Benchmark"], loc='best');

plt.show()
