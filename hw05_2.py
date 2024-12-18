import numpy as np
import matplotlib.pyplot as plt

### Data
units_sold = np.array(
    [115., 121., 124., 110., 119., 128., 166., 173., 179., 149., 156., 167.]
    ) #amount of units sold in the past months
month_goal = 13
months = range(1,13)

periodicity = 4

L_ini = 115.0
T_ini = 6.4
S_ini = np.ones(periodicity) 

alpha = 0.1
beta = 0.2
gamma = 0.3

### Processing

#init
L = L_ini
T = T_ini
S = S_ini

# update parameters for all of data
for idx, d_realized in enumerate(units_sold):
    L_old = L
    seasonality = S[idx % periodicity] # $S_{t+1}$ in slides

    L = alpha*(d_realized/seasonality) \
        + (1-alpha)*(L + T)
    T = beta*(L-L_old) + (1-beta)*T 

    S[idx % periodicity] = gamma*d_realized/L + (1-gamma)*seasonality #note: just overwrite old value as S is periodic!

# predict next month
prediction = (L+T)*S[-1] #l=1

print(f"Prediciton for Month {month_goal}: \t{round(prediction)}")
