"""Marketsimcode.py"""
#improved version of your marketsim code that accepts a "trades" data frame (instead of a file).

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data

def author():
    return 'sbaek47'

def compute_portvals(dataframe, start_val=100000, commission=0, impact=0):
    df = dataframe.sort_index()
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
    trades=prices.copy()
    trades[trades != 0] = 0

    for i in range(len(df)):
        trades[df['Symbol'][i]][df.index[i]] = df['Shares'][i] +trades[df['Symbol'][i]][df.index[i]]

    for i in range(len(df)):
        trades['Cash'][df.index[i]] += (prices[df['Symbol'][i]][df.index[i]] * - df['Shares'][i])

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


if __name__ == "__main__":
    test_code()
