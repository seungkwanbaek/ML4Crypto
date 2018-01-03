"""
#indicators.py
#Implements indicators as functions that operate on dataframes.

This code is not used explicitly, but it's borrowed in Strategy Learner as Manual Strategy

Seungkwan Bryan Baek
sbaek47
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data

def author():
    return 'sbaek47'

"""
#1. SMA: Simple Moving Average
#Arithmetic moving average calculated by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods
#SMA[t] = (price [t] / price[t - n:t].mean()) - 1

#2. Bollinger Bands
#Upper and Lower bands of 2 std dev. from SMA indicating regions of low and high volatility
#for low volatility stocks or stocks that are currently experiencing low volatility - you probably want to use a smaller number for that trigger (the price trigger?) and for high volatility a larger number.
#BB[t] = (price[t] - SMA[t]) / (2 * Std[t])

#3. Momentum
#Over a number of days, how much the price changed.
#momentum[t] = (price[t] / price[t-n]) - 1

#4. EMA: Exponential Moving Average
#moving average with more weight given to the latest data.
#First, calculate the SMA.
#Second, calculate the multiplier for weighting the EMA.
(2/(selected time period + 1))
#Finally, calculate the current EMA.
(Closing price-EMA(previous day)) x multiplier + EMA(previous day)
"""

def indicators(window, min_periods):
    syms = ['JPM']
    start_date_train = dt.datetime(2008,01,01)
    end_date_train = dt.datetime(2009,12,31)

    dates = pd.date_range(start = start_date_train, end = end_date_train)
    #Get SPY and JPM
    prices_all = get_data(syms, dates)
    #normalize the data
    norm_prices_all = prices_all.divide(prices_all.ix[0])

####################1. SMA###############################################

    norm_prices_all['SMA'] = pd.rolling_mean(norm_prices_all['JPM'], window = window, min_periods = min_periods)
    norm_prices_all['Price/SMA'] = norm_prices_all['JPM'] / norm_prices_all['SMA']

####################2. Bollinger Bands ##############################

    rolling_std = pd.rolling_std(norm_prices_all['JPM'], window = window, min_periods = min_periods)
    norm_prices_all['bollinger_up'] = (rolling_std * 2) + norm_prices_all['SMA']
    norm_prices_all['bollinger_down'] = (rolling_std * -2) + norm_prices_all['SMA']

####################3. Momentum ##############################

    norm_prices_all['momentum'] = norm_prices_all['JPM'].pct_change(periods = window, freq = 'D')

####################4. Exponential Moving Average ######################

    norm_prices_all['EMA'] = pd.ewma(norm_prices_all['JPM'], span = window, min_periods = min_periods)
    norm_prices_all['Price/EMA'] = norm_prices_all['JPM'] / norm_prices_all['EMA']

    return norm_prices_all
###############################################################################
def test_code():

    df = indicators(window = 5, min_periods = 5)

    plot_data(df[['JPM','SMA', 'Price/SMA']], title="#1. SMA of JPM", xlabel="Date", ylabel="Normalized Price")

    plot_data(df[['JPM','bollinger_up', 'bollinger_down']], title="#2. JPM Bollinger Bands", xlabel="Date", ylabel="Normalized Price")

    plot_data(df[['JPM', 'momentum']], title="#3. JPM Momentum", xlabel="Date", ylabel="Normalized Price")

    plot_data(df[['JPM','EMA', 'Price/EMA']], title="#4. EMA of JPM", xlabel="Date", ylabel="Normalized Price")
############################################################
if __name__ == "__main__":
    test_code()
