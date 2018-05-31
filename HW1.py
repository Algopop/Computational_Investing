'''
Created on March, 22, 2018

@author: Leif Buscher
@contact: leif.buscher@gmx.de
@summary: Computational Investing - Homework 1
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(dt_start, dt_end, ls_symbols, lf_port_alloc):

    # Formatting timestamps
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating dataset, read in closing price and create dictionary
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices and calculate daily portfolio returns
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    na_daily_rets = na_normalized_price.copy()
    tsu.returnize0(na_daily_rets)
    na_daily_portrets = np.sum(na_daily_rets * lf_port_alloc, axis=1)
    
    # Calculate portfolio returns and estimate statistics
    mean_portret = np.mean(na_daily_portrets)
    port_vol = np.std(na_daily_portrets)
    port_sharpe = np.sqrt(252) * mean_portret / port_vol
    cum_portrets = np.cumprod(na_daily_portrets + 1)
    cum_portret = cum_portrets[-1]

    return port_vol, mean_portret, port_sharpe, cum_portret

def print_portstats(dt_start, dt_end, ls_symbols, lf_port_alloc):
    port_vol, mean_portret, port_sharpe, cum_portret = simulate(dt_start, dt_end, ls_symbols, lf_port_alloc)
    print "Start Date: " , dt_start
    print "End Date: " , dt_end
    print "Symbols: " , ls_symbols
    print "Optimal Allocation: " , lf_port_alloc
    print "Sharpe Ration: " , port_sharpe
    print "Volatility: " , port_vol
    print "Average Daily Return: " , mean_portret
    print "Cumulative Return: " , cum_portret

def alloc_optimizer(dt_start, dt_end, ls_symbols):
    max_port_sharpe = -1
    max_port_alloc = [0.0, 0.0, 0.0, 0.0]
    for i in range(0,11,1):
        for j in range(0,11,1):
            for k in range(0,11,1):
                for l in range (0,11,1):
                    if (i + j + l + k) == 10:
                        lf_port_alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                        port_vol, mean_portret, port_sharpe, cum_portret = simulate(dt_start, dt_end, ls_symbols, lf_port_alloc)
                        if port_sharpe > max_port_sharpe:
                            max_port_sharpe = port_sharpe
                            max_port_alloc = lf_port_alloc
    return max_port_alloc


# Defining portfolio, time horizon and portfolio weights to start with
ls_symbols = ['C', 'GS', 'IBM', 'HNZ']
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
lf_port_alloc = [0.0, 0.0, 0.0, 0.0]

max_port_alloc = alloc_optimizer(dt_start, dt_end, ls_symbols)
print_portstats(dt_start, dt_end, ls_symbols, max_port_alloc)
