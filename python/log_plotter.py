#this file will plot all the data in the data folder in a log log plot
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def configure_plot(ax):
    ax.set_xlabel('t')
    ax.set_ylabel(r'$\rho(t)$')
    ax.set_title('Density of the system as a function of time')    

    #set the size of the labels
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    plt.legend(fontsize=16)

    # set the axis to log scale
    ax.set_xscale('log')
    ax.set_xlim(1e0 , 1e2)
    ax.set_yscale('log')
    ax.set_ylim(1e-1, 2e0)

    #add a legend
    ax.legend()

def plotter():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data for CP
    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    dir_path = os.path.join(root_path, 'data/bachelor_process/output') # regular data for BP
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling


    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # creating best fit variables
    best_r_squared = 0
    best_alpha = 0
    best_b = 0
    critical_lambda = 0
    
     #create the figure and the axes
    fig, ax = plt.subplots()
    
    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # Create an empty DataFrame to store all the data
        data = pd.DataFrame()

        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #get label from file name
        m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        infection_rate = float(m.group(1))
        label = r'$\lambda = $' + m.group(1)

        # add the dataframe to the plot
        ax.plot(data['t'], data['density'], label=label)

        # do a linear fit for t > 10
        x = np.log(data['t'][1:])
        y = np.log(data['density'][1:])
        # do a linear fit
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        # calculate the r squared value
        r_squared = r_value**2
        # if the r squared value is better than the previous one, save the values
        if r_squared > best_r_squared:
            best_r_squared = r_squared
            best_alpha = slope
            best_b = intercept
            critical_lambda = infection_rate
        
    # create linespace for x values
    x = np.linspace(0, 1e2, 1000)

    alpha = best_alpha
    b = best_b
    y = alpha*x+b
    x_exp = np.exp(x)
    y_exp = np.exp(y)

    # plot the line in black
    label = f"y = {alpha}x + {b}"
    ax.plot(x_exp, y_exp, color='black', label=label)
    print(f"best alpha: {best_alpha} with r squared: {best_r_squared} and b: {best_b} for lambda: {critical_lambda}")

    configure_plot(ax)

    #show the plot
    plt.show()

if __name__ == '__main__':
    plotter()
