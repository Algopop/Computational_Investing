import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
 
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import math
from math import sqrt

port_syms = ["GOOG", "AAPL", "GLD", "XOM"]

port_alloc = np.ones((1,4))
alloc = np.arange(0,1.1,0.1)

for i in alloc:
	port_alloc * i

if np.sum(port_alloc) = 1:
	print port_alloc
else:
	continue

for x in port_syms:
	port_alloc(alloc) = 1
	print port_syms
		
		

c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)


def simulate(dt_start, dt_end, port_syms, port_alloc):

	dt_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
	
	c_dataobj = da.DataAccess('Yahoo')
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, port_syms, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
 
	na_price = d_data['close'].values

	na_norm_price = na_price / na_price[0,:]

	na_rets = na_norm_price.copy()
	tsu.returnize0(na_rets)

	na_portrets = np.sum(na_rets * port_alloc, axis=1)
	na_port_total = np.cumprod(na_portrets)

	port_vol = np.std(na_portrets, axis=0)

	port_mean = np.mean(na_portrets, axis=0)

	port_daily_rets = np.average(na_portrets, axis=0)
	
	port_sharpe = (port_mean * 252) / (port_vol * sqrt(252))
	
	print "Symbols:" + str (port_syms)
	print "Optimal Allocation:" + str (port_alloc)
	print "Sharpe Ratio:" + str (port_sharpe)
	print "Volatility (stdev of daily returns:" + str (port_vol)
	print "Average Daily Return:" +"   " + str (port_mean)
		
print simulate(dt_start, dt_end, ["AAPL", 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])


