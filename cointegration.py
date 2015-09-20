'''
Author: Isaac Drachman
Date:   09/20/2015
Description:
Some small routines for analyzing cointegration between securities.
'''

import pandas
import pandas.io.data

from statsmodels.tsa.stattools import adfuller
from statsmodels.api import OLS

# Downloads prices for tickers within given date range.
def prices(tickers, startdate, enddate):
	df = pandas.DataFrame(columns=tickers)
	for ticker in tickers:
		df[ticker] = pandas.io.data.DataReader(ticker, "yahoo", start=startdate, end=enddate)["Adj Close"]
	return df

# Get last price.
def quotes(tickers):
	ids = ",".join(tickers)
	url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=ssl1n"%ids
	return pandas.read_csv(url,header=None,names=["symbol","price","name"],index_col=0)

# Compute ordinary least squares regression on spread between two securities.
# We have the fit: S1 ~ beta * S2 (where S1 and S2 are our stocks)
def spreads(df, ticker1, ticker2):
	beta = OLS(df[ticker1], df[ticker2]).fit().params.iloc[0]
	return df[ticker1] - beta * df[ticker2], beta

# Run ADF test on mean reversion for the spread.
def routine(ticker1, ticker2, startdate, enddate):
	df = prices([ticker1, ticker2], startdate, enddate)
	spread, beta = spreads(df, ticker1, ticker2)
	# Return historical spreads, beta, and p-value for ADF test.
	return spread, beta, adfuller(spreads)[1]
