"""
Compare StrategyLearner with different value of impact

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

def StrategyLearnerPortfolioValue(df, impact):
    df = df.assign(Cash = 0)

    for i in range(len(df)):
        if (df[sym][i] > 0):
            df['Cash'][i] += (1 + impact) * (prices[sym][i] * - df[sym][i])
        else:
            df['Cash'][i] += (1 - impact) * (prices[sym][i] * - df[sym][i])

    for j in range(len(df.columns)):
            stock = 0
            for i in range(len(df)):
                df.iloc[i,j] = stock + df.iloc[i,j]
                stock = df.iloc[i,j]

    df['Cash'] = df['Cash'] + sv

    value = df * prices
    df_Strategy = value.sum(axis=1)

    return df_Strategy
###############################################################
impact_values = [0, 0.005 , 0.01, 0.015, 0.02, 0.025, 0.03]

Metric_df = pd.DataFrame()
Metric_df['impact'] = impact_values
Metric_df = Metric_df.set_index('impact')
Metric_df = Metric_df.assign(Trades = 1.0)
Metric_df = Metric_df.assign(CR = 1.0)
Metric_df = Metric_df.assign(SR = 1.0)
Metric_df = Metric_df.assign(ADR = 1.0)
Metric_df = Metric_df.assign(PortfolioValue = 1.0)

sv = 100000
sd_train = dt.datetime(2008,01,01)
ed_train = dt.datetime(2009,12,31)

sym = "JPM"

dates = pd.date_range(sd_train, ed_train)
prices = ut.get_data([sym], dates, False)
prices = prices.assign(Cash = 1.0)
prices = prices.dropna(axis=0)

#Strategy Learner
for impact in impact_values:

    learner = sl.StrategyLearner(verbose = False, impact = impact)
    learner.addEvidence(symbol = sym, sd = sd_train, ed = ed_train, sv = sv)
    orders_Strategy = learner.testPolicy(symbol = sym, sd = sd_train, \
        ed = ed_train, sv = sv)

    no_trades = orders_Strategy[sym].astype(bool).sum(axis=0)

    df_Strategy = StrategyLearnerPortfolioValue(orders_Strategy, impact)

    Strategy_cr, Strategy_adr, Strategy_sddr, Strategy_sr = ms.stat_summary(df_Strategy)

    Metric_df['Trades'][impact] = no_trades
    Metric_df['CR'][impact] = Strategy_cr
    Metric_df['ADR'][impact] = Strategy_adr
    Metric_df['SR'][impact] = Strategy_sr
    Metric_df['PortfolioValue'][impact] = df_Strategy[-1]

    # print "Impact: {}".format(impact)
    # print
    # print "Number of trades for Strategy: {}".format(no_trades)
    # print
    # print "Cumulative Return of Strategy: {}".format(Strategy_cr)
    # print
    # print "Average Daily Return of Strategy: {}".format(Strategy_adr)
    # print
    # print "SR of Strategy: {}".format(Strategy_sr)
    # print
    # print "Final Portfolio Value of Strategy: {}".format(df_Strategy[-1])

###############################################################################

print Metric_df

ut.plot_data(Metric_df[['CR', 'SR']], title="Experiment 2: Effects of Impact on CR and SR", xlabel="Impact", ylabel="Values")

ut.plot_data(Metric_df[['PortfolioValue']], title="Experiment 2: Effects of Impact on Portfolio Value", xlabel="Impact", ylabel="USD")

ut.plot_data(Metric_df[['Trades']], title="Experiment 2: Effects of Impact on the Number of Trades", xlabel="Impact", ylabel="Count")

###############################################################################
