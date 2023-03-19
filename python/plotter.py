#this file will plot all the data in the data folder in a log log plot

import os
import pandas as pd
import matplotlib.pyplot as plt

# Set the directory path where the CSV files are located
dir_path = 'C:/Users/kheyn/Documents/uhasselt/eindproject/22-23/data'

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# Loop through all the CSV files and append the data to the DataFrame
for csv_file in csv_files:
    # Create an empty DataFrame to store all the data
    data = pd.DataFrame()

    csv_path = os.path.join(dir_path, csv_file)
    data = pd.read_csv(csv_path)

    # add the dataframe to the plot
    plt.plot(data['t'], data['density'], label=csv_file)

# Plot the data
plt.xlabel('t')
plt.ylabel('density')
plt.title('All CSV Data')

#set the axis to log scale
plt.xscale('log')
plt.yscale('log')

#add a legend
plt.legend()

#show the plot
plt.show()
