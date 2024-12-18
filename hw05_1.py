import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

### Data
units_sold = np.array(
    [115., 121., 124., 110., 119., 128., 166., 173., 179., 149., 156., 167.]
    ) #amount of units sold in the past months
months = range(1,13)

# plot data
fig = plt.figure(figsize=(8, 6))
ax = fig.subplots()
ax.grid(True)
ax.set_xlabel("Month")
ax.set_ylabel("Units")
ax.set_title("Static Demand Forecast")


ax.plot(months, units_sold, label="Units Sold")

### PROCESS

# remove seasonality
periodicity = 4 #periodicity aka. kernel length
if periodicity % 2 != 0: #even kernel
    kernel = np.ones(periodicity)/periodicity
else:
    kernel = np.ones(periodicity+1)/periodicity
    kernel[0] *= 0.5
    kernel[-1] *= 0.5

no_seasonality = np.convolve(units_sold,kernel,mode='valid') #remove seasonality
valid_months = range(1+periodicity//2,1+len(no_seasonality)+periodicity//2) #months w/o seasonality (that are valid)

# add seasonality removed to plot
ax.plot(valid_months,no_seasonality,
        label="Units Sold w/o seasonality")

# do linear regression to find L T
T,L, *_ = linregress(valid_months,no_seasonality)

# add linear prediciton just for fun
all_months = range(1,17)
goal_months = range(13,17)
ax.plot(all_months,L+all_months*T,label="Linear Predictions ")

# find seasonality factors
linear_past = L+months*T
seasonality_past = units_sold/linear_past #all factors
num_full_iterations = len(seasonality_past)//periodicity
seasonailty = np.array([np.sum(seasonality_past[offset::periodicity])
               for offset in range(num_full_iterations+1)])/num_full_iterations #sum iteratively and normalize

# do estimation of future
prediction_noseason = L+T*goal_months
seasonality_tiled = np.tile(seasonailty,len(goal_months)//len(seasonailty)+1)[:len(goal_months):]
prediction = prediction_noseason*seasonality_tiled

# add prediction to plot
ax.plot(goal_months,prediction,label="Forecast")
print("Predictions")
for i,m in enumerate(goal_months):
    print(f"{m}:\t{round(prediction[i])}")

# show plot
ax.legend()
fig.savefig("./out/hw05_1.png",format="png")
plt.show()



