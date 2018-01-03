"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'sbaek47'

def compute_portvals(dataframe, start_val, commission, impact):
    #sort the csv by date
    df = pd.read_csv(orders_file, index_col='Date')
    df = df.sort_index()

    start_date = df.index[0]
    end_date = df.index[len(df)-1]

    #convert SELL shares to negative stocks
    df['Shares'][df['Order'].str.contains("SELL")] = -df['Shares'][df['Order'].str.contains("SELL")]
    stocks = df.Symbol.unique()

#DF1
    dates = pd.date_range(start_date, end_date)
    prices = get_data(stocks, dates, False)
    prices = prices.assign(Cash = 1.0)
    prices = prices.dropna(axis=0)

#DF2
    trades = prices.copy()
    trades[trades != 0] = 0

    for i in range(len(df)):
        trades[df['Symbol'][i]][df.index[i]] = df['Shares'][i] +trades[df['Symbol'][i]][df.index[i]]

    for i in range(len(df)):
        if (df['Order'][i] == "BUY"):
            trades['Cash'][df.index[i]] += (1+impact)*(prices[df['Symbol'][i]][df.index[i]] * - df['Shares'][i])-commission
        else:
            trades['Cash'][df.index[i]] += (1-impact) * (prices[df['Symbol'][i]][df.index[i]] * - df['Shares'][i])-commission

#DF3
    holdings = trades.copy()
    for j in range(len(holdings.columns)):
        stock = 0
        for i in range(len(holdings)):
            holdings.iloc[i,j] = stock + holdings.iloc[i,j]
            stock = holdings.iloc[i,j]
    holdings['Cash'] = holdings['Cash']+start_val

    value = holdings * prices

#DF4
    portvals = value.sum(axis=1)
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding this function will not be called.
    # Define input parameters

    of = "./orders/orders-12.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
