"""MLT: Utility code."""

import os
import pandas as pd
from scipy import stats
import numpy as np


def symbol_to_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol."""
    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", '../data/')
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates, addSPY=True, colname = 'Adj Close'):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', colname], na_values=['nan'])
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    import matplotlib.pyplot as plt
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def get_orders_data_file(basefilename):
    return open(os.path.join(os.environ.get("ORDERS_DATA_DIR",'orders/'),basefilename))

def get_learner_data_file(basefilename):
    return open(os.path.join(os.environ.get("LEARNER_DATA_DIR",'Data/'),basefilename),'r')

def get_robot_world_file(basefilename):
    return open(os.path.join(os.environ.get("ROBOT_WORLDS_DIR",'testworlds/'),basefilename))
######################################################
def entropy(class_y):

    zero = float( np.count_nonzero(class_y) )
    one = float( len(class_y) - np.count_nonzero(class_y) )

    if zero == 0 or one == 0:
        return 0

    zeros = zero/len(class_y)
    ones = one/len(class_y)

    entropy = -zeros*np.log2(zeros)-(ones)*np.log2(ones)
    return entropy


def partition_classes(X, y, split_attribute, split_val):

    if isinstance(split_val, basestring):
        X_left = [t for t in X if t[split_attribute] == split_val]
        X_right = [t for t in X if t[split_attribute] != split_val]

        y_left = [y[X.index(t)] for t in X if t[split_attribute] == split_val]
        y_right = [y[X.index(t)] for t in X if t[split_attribute] != split_val]

        return (X_left, X_right, y_left, y_right)

    else:
        X_left = [t for t in X if t[split_attribute] <= split_val]
        X_right = [t for t in X if t[split_attribute] > split_val]


        y_left = [y[X.index(t)] for t in X if t[split_attribute] <= split_val]
        y_right = [y[X.index(t)] for t in X if t[split_attribute] > split_val]

        return (X_left, X_right, y_left, y_right)


def information_gain(previous_y, current_y):

    PL = 1. * len(current_y[0])/len(previous_y)
    PR = 1. *len(current_y[1])/len(previous_y)

    HL = entropy(current_y[0])
    HR = entropy(current_y[1])

    H = entropy(previous_y)

    info_gain = H - (HL * PL + HR * PR)

    return info_gain
