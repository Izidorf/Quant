import numpy as np
cimport numpy as np
from collections import namedtuple

fields = ["spot", "riskfree", "sigma", "maturity", "timesteps", "samples", "strike", "knockout"]
Option = namedtuple("Option", fields)

# Asian call.
cdef np.float64_t payoff(np.ndarray[np.float64_t, ndim=1] samples, object option):
	return max(samples.mean() - option.strike, 0.0)

# Up-and-out asian barrier call.
cdef np.float64_t barrierpayoff(np.ndarray[np.float64_t, ndim=1] samples, object option):
	for t in range(1, option.timesteps+1):
		if samples[t] >= option.knockout:
			return 0.0
	return payoff(samples, option)

cdef np.ndarray[np.float64_t, ndim=1] trajectory(object option):
	cdef float dt = option.maturity / option.timesteps
	cdef np.ndarray[np.float64_t, ndim=1] samples = np.zeros(option.timesteps+1)
	samples[0] = option.spot
	for t in range(1, option.timesteps+1):
		samples[t] = samples[t-1] * (1. + option.riskfree*dt + option.sigma*np.sqrt(dt)*np.random.normal()) 
	return samples

cdef np.ndarray[np.float64_t, ndim=2] montecarlo(object option):
	cdef np.ndarray[np.float64_t, ndim=2] samples = np.zeros((option.samples, option.timesteps+1))
	for k in range(option.samples):
		samples[k] = trajectory(option)
	return samples

cpdef np.float64_t evaluate(object option):
	cdef np.ndarray[np.float64_t, ndim=2] samples = montecarlo(option)
	cdef np.ndarray[np.float64_t, ndim=1] premiums = np.zeros(option.samples)
	for k in range(option.samples):
		premiums[k] = barrierpayoff(samples[k], option)
	return np.exp(-option.riskfree*option.maturity)*premiums.mean()