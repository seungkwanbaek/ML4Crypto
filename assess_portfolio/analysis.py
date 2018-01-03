"""Analyze a portfolio.
Seungkwan "Bryan" Baek
sbaek47
Project 1
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns=df.copy()
    daily_returns[1:]=(daily_returns[1:]/daily_returns[:-1].values)-1
    daily_returns.ix[0] = 0
    return daily_returns

def assess_portfolio(sd, ed, syms, allocs, sv, rfr, sf, gen_plot):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    #prices_all is a df

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    #TODO: Compute the statistics

    #normalize the price data
    normed=prices.divide(prices.ix[0])

    alloced=normed*allocs
    pos_vals=alloced*sv

    #sum up by day
    portfolio_value=pos_vals.sum(axis=1)

    #Cumulative Return
    cr=(portfolio_value[-1]/portfolio_value[0])-1

    #compute daily return
    daily_rets=compute_daily_returns(portfolio_value)
    #get rid of first daily return which is 0
    daily_rets=daily_rets[1:]

    #Average Daily Return
    adr=daily_rets.mean()

    #Std dev of daily return
    sddr=daily_rets.std()

    #Sharpe Ratio
    sr=np.sqrt(sf)*(adr-rfr)/(sddr)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    # Add code here to properly compute end value
    ev = portfolio_value[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252.0

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        rfr=risk_free_rate,\
        sf=sample_freq,\
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
