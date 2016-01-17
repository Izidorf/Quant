# Quant
Assorted quantitative finance related code snippets.

## montecarlo.pyx, setup.py, demo.py
- Monte Carlo options pricing in Cython
- Currently prices Asian calls (including up-and-out barrier)
- Use <code>python setup.py build_ext --inplace</code> to build the code
- The script demo.py implements some tests

## cointegration.py
- Runs ADF test for mean-reversion on historical spreads between two securities.
- Requires pandas and statsmodels.

## impliedvol.py
- Computes implied volatility for options using Black Scholes valuation.
- Requires scipy.

## Monte Carlo Options pricing
- Also see my MonteCarloOptions project on Github
- A CUDA/C++ MC simulation for black scholes options pricing
