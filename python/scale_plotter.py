#this file will plot all the data in the data folder in a scaled log log plot
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def scale_plotter():
    # defining parameters
    alpha = -0.1598
    lambda_critical = 3.29785
    nu_parallel = 1.73383 #this is our guess

     # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, 'data\scale_data')

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # create an empty DataFrame to store all the data
        data = pd.DataFrame()

        # define lambda from file name
        simulated_lambda = float(csv_file[7:15])

        # read the csv file
        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        # scale the data
        x_axis = data['t'] * (simulated_lambda - lambda_critical)**nu_parallel
        y_axis = data['density'] * (data['t'] ** alpha)

        # add the dataframe to the plot
        plt.plot(x_axis, y_axis, label=csv_file)

    # Plot the data
    plt.xlabel('t')
    plt.ylabel('density')
    plt.title('All CSV Data')

    #set the axis to log scale
    plt.xscale('log')
    plt.xlim(1e-4, 1e1)
    plt.yscale('log')
    plt.ylim(1e-3, 1e0)

    #add a legend
    plt.legend()

    #show the plot
    plt.show()


if __name__ == '__main__':
    scale_plotter()