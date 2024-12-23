import numpy as np

### Data
demand = np.array(
    [1000,1200,1300,1100]
    ) #amount of units sold in the past months

periodicity = 4

L_ini = 1000
T_ini = 40
S_ini = [1.0,1.1,1.2,0.9] 

alpha = 0.2
beta = 0.5
gamma = 0.5

### Processing

#init
L = L_ini
T = T_ini
S = S_ini

# update parameters for all of data
for idx, d_realized in enumerate(demand):
    L_old = L
    seasonality = S[idx % periodicity] # $S_{t+1}$ in slides

    L = alpha*(d_realized/seasonality) \
        + (1-alpha)*(L + T)
    T = beta*(L-L_old) + (1-beta)*T 

    S[idx % periodicity] = gamma*d_realized/L + (1-gamma)*seasonality #note: just overwrite old value as S is periodic!

    print(f"Results for {idx}")
    print(f"Level:\t{round(L,1)}")
    print(f"Trend:\t{round(T,1)}")
    print(f"Forecast:\t{round((L+T)*seasonality,1)}") #USE OLD SEASONALITY

print(np.round(S,2))
