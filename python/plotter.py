#this file will plot all the data in the data folder in a log log plot
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Set the directory path where the CSV files are located
dir_path = 'D:/UHasselt/eindwerk/bachelor_kristof_heyndels_fysica_22_23/data'

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# Loop through all the CSV files and append the data to the DataFrame
for csv_file in csv_files:        
    # Create an empty DataFrame to store all the data
    data = pd.DataFrame()

    csv_path = os.path.join(dir_path, csv_file)
    print(csv_path)
    data = pd.read_csv(csv_path)

    # add the dataframe to the plot
    plt.plot(data['t'], data['density'], label=csv_file)


#plot line with slope -0.1598 in log log scale

#create linespace for x values
x = np.linspace(0, 1e2, 1000)
#calculate y values
y = -0.1598*x-0.375
x_exp = np.exp(x)
y_exp = np.exp(y)
#plot the line
plt.plot(x_exp, y_exp, label='slope -0.1598')


# Plot the data
plt.xlabel('t')
plt.ylabel('density')
plt.title('All CSV Data')

#set the axis to log scale
plt.xscale('log')
plt.xlim(1e0, 1e2)
plt.yscale('log')
plt.ylim(1e-1, 1)

#add a legend
plt.legend()

#show the plot
plt.show()
