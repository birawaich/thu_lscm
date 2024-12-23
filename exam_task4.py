import numpy as np

d = [600,500,550,750,650,550,700,550]
kernel = np.ones(3)/3

forecast = np.convolve(d,kernel,mode='valid')

forecast_cut = forecast[0:5:]
demand_cut = d[3::]

error = forecast_cut-demand_cut

error_abs = np.abs(error)
for n in range(6):
    # mad = sum(error_abs[0:n+1])/(n+1)
    # print(mad)
    bias = sum(error[0:(n+1)])
    print(bias)


print("DONE")
