#BestPossibleStrategy.py

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data
from marketsimcode import compute_portvals

def author():
    return 'sbaek47'

##########BEST POSSIBLE STRATEGY################################
def testPolicy(symbol, sd, ed, sv):
    dates= pd.date_range(start=sd, end=ed)
    prices_all = get_data([symbol], dates)

    prices_all['Shares'] = 0
    prices_all['Order'] = ""
    prices_all['Symbol'] = "JPM"

    shares = 0
    for i in range(len(prices_all)-1):
        if prices_all['JPM'][i+1] > prices_all['JPM'][i]:
            while shares < 1000:
                shares += 1000
                prices_all['Shares'][i] += 1000
                prices_all['Order'][i] = "BUY"
        else:
            while shares > -1000:
                shares -= 1000
                prices_all['Shares'][i] += 1000
                prices_all['Order'][i] = "SELL"

    bestdf = prices_all[['Symbol','Shares', 'Order']].copy()

    return bestdf
#########BENCHMARK##############################
def testPolicy_benchmark(symbol, sd, ed, sv):
    dates= pd.date_range(start=sd, end=ed)
    prices_all = get_data([symbol], dates)

    prices_all['Shares'] = 0
    prices_all['Order'] = ""
    prices_all['Symbol'] = "JPM"

    benchmark = prices_all[['Symbol','Shares', 'Order']].copy()
    benchmark['Shares'][0] = 1000
    benchmark['Order'][0] = "BUY"

    return benchmark

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns=df.copy()
    daily_returns[1:]=(daily_returns[1:]/daily_returns[:-1].values)-1
    daily_returns.ix[0] = 0
    return daily_returns

#######################################################
def test_code():
    sv = 100000
    bestpossible_orders = testPolicy(symbol = "JPM", sd=dt.datetime(2008,01,01), ed=dt.datetime(2009,12,31), sv = sv)
    benchmark_orders = testPolicy_benchmark(symbol = "JPM", sd=dt.datetime(2008,01,01), ed=dt.datetime(2009,12,31), sv = sv)

    beststrategy_df = compute_portvals(bestpossible_orders, start_val=sv, commission=0, impact=0)
    benchmark_df = compute_portvals(benchmark_orders, start_val = sv, commission=0, impact=0)
###############################################################################
    norm_beststrategy_df = beststrategy_df.divide(beststrategy_df.ix[0])

    daily_rets_best=compute_daily_returns(norm_beststrategy_df)
    daily_rets_best = daily_rets_best[1:]
    #Cumulative return
    cum_return_beststrategy=(norm_beststrategy_df[-1]/norm_beststrategy_df[0])-1

    #Average Daily Return
    adr_best=daily_rets_best.mean()

    #Std dev of daily return
    sddr_best=daily_rets_best.std()

    #Sharpe Ratio
    sr_best=np.sqrt(252.0)*(adr_best-0)/(sddr_best)
###############################################################################
    norm_benchmark_df = benchmark_df.divide(benchmark_df.ix[0])

    daily_rets_benchmark=compute_daily_returns(norm_benchmark_df)
    daily_rets_benchmark = daily_rets_benchmark[1:]
    #Cumulative return
    cum_return_benchmark=(norm_benchmark_df[-1]/norm_benchmark_df[0])-1

    #Average Daily Return
    adr_benchmark=daily_rets_benchmark.mean()

    #Std dev of daily return
    sddr_benchmark=daily_rets_benchmark.std()

    #Sharpe Ratio
    sr_benchmark=np.sqrt(252.0)*(adr_benchmark-0)/(sddr_benchmark)

    print "Cumulative Return of Best: {}".format(cum_return_beststrategy)
    print "Cumulative Return of Benchmark : {}".format(cum_return_benchmark)
    print
    print "Standard Deviation of Best: {}".format(sddr_best)
    print "Standard Deviation of Benchmark : {}".format(sddr_benchmark)
    print
    print "Average Daily Return of Best: {}".format(adr_best)
    print "Average Daily Return of Benchmark : {}".format(adr_benchmark)
    print
    print "SR of Best: {}".format(sr_best)
    print "SR of Benchmark : {}".format(sr_benchmark)
    print
    print "Final Portfolio Value of Best: {}".format(beststrategy_df[-1])
    print "Final Portfolio Value of Benchmark : {}".format(benchmark_df[-1])

    ax = norm_beststrategy_df.plot(title="BestPossibleStrategy vs. Benchmark", fontsize=12, color="Black")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")

    norm_benchmark_df.plot(ax=ax, color="Blue")
    ax.legend(["BestPossibleStrategy", "Benchmark"], loc='best');

    plt.show()


if __name__ == "__main__":
    test_code()
