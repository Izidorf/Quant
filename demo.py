import sys
from montecarlo import Option, evaluate

if __name__ == "__main__":
	S0    = 100.00
	r     = 0.0050
	sigma = 0.10
	T     = 1.0
	K	  = 100.00
	B	  = 120.00
	N     = 1000
	M     = int(sys.argv[1])
	
	stock = Option(S0, r, sigma, T, N, M, K, B)
	premium = evaluate(stock)
	print "premium: $ %0.4f" % (premium)