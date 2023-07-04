#this file will plot all the data in the data folder in a log log plot
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotter():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, 'data')

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # Create an empty DataFrame to store all the data
        data = pd.DataFrame()

        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #get label from file name
        label = r'$\lambda = $' + csv_file[7:14]

        # add the dataframe to the plot
        plt.plot(data['t'], data['density'], label=label)


    #plot line with slope -0.1598 in log log scale
    #create linespace for x values
    x = np.linspace(0, 1e2, 1000)
    #calculate y values
    y = -0.16*x-0.375
    x_exp = np.exp(x)
    y_exp = np.exp(y)
    #plot the line in black
    plt.plot(x_exp, y_exp, color='black', label=r'$y=-0.16x+b$')


    # Plot the data
    plt.xlabel('t')
    plt.ylabel(r'$\rho(t)$')
    plt.title('Density of the system as a function of time')

    #set the size of the labels
    plt.tick_params(axis='both', which='major', labelsize=12)
    ax = plt.gca()
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    plt.legend(fontsize=16)

    #set the axis to log scale
    plt.xscale('log')
    plt.xlim(1e0, 1e2)
    plt.yscale('log')
    plt.ylim(1e-1, 1)

    #add a legend
    plt.legend()

    #show the plot
    plt.show()

if __name__ == '__main__':
    plotter()
