#ManualStrategy.py

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data
#from marketsimcode import compute_portvals

def author():
    return 'sbaek47'

##########Manual STRATEGY################################
def testPolicy(symbol, sd, ed, sv):
    dates= pd.date_range(start=sd, end=ed)
    prices_all = get_data([symbol], dates)

    norm_prices_all = prices_all.copy()
    norm_prices_all = norm_prices_all.divide(norm_prices_all.ix[0])
####################1. SMA###############################################
    lookback = 14

    sma = pd.rolling_mean(norm_prices_all['JPM'], window = lookback, min_periods = lookback)
    price_sma = norm_prices_all['JPM'] / sma

####################2. Bollinger Bands ##############################
    rolling_std = pd.rolling_std(norm_prices_all['JPM'], window = lookback, min_periods = lookback)


    up = (rolling_std * 2) + sma
    down = (rolling_std * -2) + sma

    #Bollinger Band %
    bbp = (norm_prices_all['JPM'] - down) / (up - down)

#####################3. EMA ##############################

    ema = pd.ewma(norm_prices_all['JPM'], span = lookback, min_periods = lookback)
    price_ema = norm_prices_all['JPM'] / ema
####################4. Momentum ##############################

    momentum = norm_prices_all['JPM'].pct_change(periods = lookback, freq = 'D')
    momentum = momentum.dropna()

####################3. Strategy Part ##############################

    orders = prices_all['JPM'].copy()
    orders.ix[:] = np.NaN

    orders[(price_ema < 0.95) & (bbp < 0) ] = 1000
    orders[(price_ema > 1.05) & (bbp > 1) ] = -1000

    ema_cross = price_ema.copy()
    ema_cross[:] = 0
    ema_cross[price_ema >= 1] = 1

    ema_cross = ema_cross.diff()
    ema_cross[0] = 0

    orders[(ema_cross != 0)] = 0
    orders.ffill(inplace=True)
    orders.fillna(0, inplace=True)

    orders= orders.diff()
    orders[0] = 0

    orders=orders.loc[(orders != 0)]

    orders_list=orders.copy()

    orders_list=orders_list.to_frame("Shares")
    orders_list['Order']=" "
    orders_list['Symbol']="JPM"
    orders_list['Shares']=1000

    for day in range(len(orders)):
        if orders[day] > 0:
            orders_list['Order'][day] = "BUY"
        elif orders[day] < 0:
            orders_list['Order'][day] = "SELL"

    return orders_list
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

#######################################################
def test_code():
    sv = 100000
    bestpossible_orders = testPolicy(symbol = "JPM", sd=dt.datetime(2008,01,01), ed = dt.datetime(2009,12,31), sv = sv)
    benchmark_orders = testPolicy_benchmark(symbol = "JPM", sd=dt.datetime(2008,01,01), ed = dt.datetime(2009,12,31), sv = sv)

    test_orders = testPolicy(symbol = "JPM", sd = dt.datetime(2010,01,01), ed = dt.datetime(2011,12,31), sv = sv)
    test_benchmark_orders = testPolicy_benchmark(symbol = "JPM", sd = dt.datetime(2010,01,01), ed = dt.datetime(2011,12,31), sv = sv)

    beststrategy_df = compute_portvals(bestpossible_orders, start_val = sv, commission = 9.95, impact = 0.005)
    benchmark_df = compute_portvals(benchmark_orders, start_val = sv, commission = 9.95, impact = 0.005)
    test_df = compute_portvals(test_orders, start_val = sv, commission = 9.95, impact = 0.005)
    test_benchmark_df = compute_portvals(test_benchmark_orders, start_val = sv, commission = 9.95, impact = 0.005)

###############################################################################
    norm_beststrategy_df = beststrategy_df.divide(beststrategy_df.ix[0])
    norm_benchmark_df = benchmark_df.divide(benchmark_df.ix[0])
    norm_test_df = test_df.divide(test_df.ix[0])
    norm_test_benchmark_df = test_benchmark_df.divide(test_benchmark_df.ix[0])

    inbest_cr, inbest_adr, inbest_sddr, inbest_sr = stat_summary(norm_beststrategy_df)
    inbench_cr, inbench_adr, inbench_sddr, inbench_sr = stat_summary(norm_benchmark_df)
    outbest_cr, outbest_adr, outbest_sddr, outbest_sr = stat_summary(norm_test_df)
    outbench_cr, outbench_adr, outbench_sddr, outbench_sr = stat_summary(norm_test_benchmark_df)

    print "Cumulative Return of In Strategy: {}".format(inbest_cr)
    print "Cumulative Return of In Benchmark : {}".format(inbench_cr)
    print "Cumulative Return of Out Strategy: {}".format(outbest_cr)
    print "Cumulative Return of Out Benchmark : {}".format(outbench_cr)
    print
    print "Standard Deviation of In Strategy: {}".format(inbest_sddr)
    print "Standard Deviation of In Benchmark : {}".format(inbench_sddr)
    print "Standard Deviation of Out Strategy: {}".format(outbest_sddr)
    print "Standard Deviation of Out Benchmark : {}".format(outbench_sddr)
    print
    print "Average Daily Return of In Strategy: {}".format(inbest_adr)
    print "Average Daily Return of In Benchmark : {}".format(inbench_adr)
    print "Average Daily Return of Out Strategy: {}".format(outbest_adr)
    print "Average Daily Return of Out Benchmark : {}".format(outbench_adr)
    print
    print "SR of In Strategy: {}".format(inbest_sr)
    print "SR of In Benchmark : {}".format(inbench_sr)
    print "SR of Out Strategy: {}".format(outbest_sr)
    print "SR of Out Benchmark : {}".format(outbench_sr)
    print
    print "Final Portfolio Value of In Strategy: {}".format(beststrategy_df[-1])
    print "Final Portfolio Value of In Benchmark : {}".format(benchmark_df[-1])
    print "Final Portfolio Value of Out Strategy: {}".format(test_df[-1])
    print "Final Portfolio Value of Out Benchmark : {}".format(test_benchmark_df[-1])
###############################################################################
    ax = norm_beststrategy_df.plot(title = "In-Sample Strategy vs. Benchmark", fontsize = 12, color = "Black")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")
    norm_benchmark_df.plot(ax=ax, color="Blue")
    #draw vert. line
    BUY = bestpossible_orders[bestpossible_orders.Order == "BUY"].index
    for xc in BUY:
        plt.axvline(x=xc, color="Green")

    SELL = bestpossible_orders[bestpossible_orders.Order == "SELL"].index
    for xc in SELL:
        plt.axvline(x=xc, color="Red")

    ax.legend(["Strategy", "Benchmark"], loc='best');

    plt.show()
###############################################################################
    bx = norm_test_df.plot(title="Out-of-Sample Strategy vs. Benchmark", fontsize=12, color="Black")
    bx.set_xlabel("Date")
    bx.set_ylabel("Normalized Price")

    norm_test_benchmark_df.plot(ax=bx, color="Blue")
    bx.legend(["Strategy", "Benchmark"], loc='best');

    plt.show()

if __name__ == "__main__":
    test_code()
