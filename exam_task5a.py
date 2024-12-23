import numpy as np

l0 = 1000
t0 = 40
s = np.array([1.0,1.1,1.2,0.9])
index = np.array(range(1,5))

forcast2023 = np.sum( (l0+t0*index)*s )
print(forcast2023)