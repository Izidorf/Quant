'''
Author: Isaac Drachman
Date:   09/20/2015
Description:
Computes implied volatility for a given option.
'''

from scipy.optimize import brentq
from scipy.stats import norm
from math import sqrt, log, exp

# Compute premium for a call using Black Scholes.
def black_scholes_call(S0, K, T, r, sigma):
	d1 = (log(S0/K) + (r + sigma**2/2)*T) / (sigma * sqrt(T))
	d2 = d1 - sigma*sqrt(T)
	return S0 * norm.cdf(d1) - exp(-r*T) * K * norm.cdf(d2)

# Compute premium for a put using BS for a
# call and Put-Call parity.
def black_scholes_put(S0, K, T, r, sigma):
	C = black_scholes_call(S0, K, T, r, sigma)
	return C - S0 - exp(-r*T) * K

# Compute implied volatiltiy for a call
# by finding the sigma s.t. C - C(sigma) = 0.
# Where C is actual premium, and C(sigma) is
# premium as defined by BS as a func of vol.
def implied_vol_call(C, S0, K, T, r):
	f = lambda sigma: C - black_scholes_call(S0, K, T, r, sigma)
	return brentq(f, 0.001, 1.00)

# Similarly for a put.
def implied_vol_put(P, S0, K, T, r):
	f = lambda sigma: P - black_scholes_put(S0, K, T, r, sigma)
	return brentq(f, 0.001, 1.00)