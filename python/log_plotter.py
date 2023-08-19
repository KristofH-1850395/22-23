# ===========================================================================================================================================
# ===Script for calculating the exponent alpha and finding the critical lambda===============================================================
# ===Plots the data in a log-log plot and look for a linear relation (dataset following a power law at the critical point)===================
# ===note: in the bachelor process, all graphs under the critical point end up following a power law (exp = 0.5) due to the mixing process===
# ===========================================================================================================================================

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scienceplots

plt.style.use(['science', 'ieee', 'no-latex'])
plt.rcParams.update({'figure.dpi': '300'})

def configure_plot(ax):    
    ax.set_xlabel('t')
    ax.set_ylabel(r'$\rho(t)$')
    # ax.set_title('Contact Process - Density vs. Time')    
    
    # add a legend
    ax.legend()

    # set the axis to log scale for the CP
    # ax.set_xscale('log')
    # ax.set_xlim(1e0, 1e2)

    # ax.set_yscale('log')
    # ax.set_ylim(0.22, 0.69)

    # set the axis to log scale for the PP
    ax.set_xscale('log')
    ax.set_xlim(2*1e0, 1e4)

    ax.set_yscale('log')
    ax.set_ylim(0.03, 1.2)

def plotter():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data for CP
    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output') # regular data for PP
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling

    dir_path = os.path.join(root_path, 'data/bachelor_process/test') # for testing

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # creating best fit variables
    best_r_squared = 0
    best_alpha = 0
    best_b = 0
    critical_lambda = 0
    fit_list = []
    
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

        # divide the density data by 0.2875842775118721
        scaled_density = data['density']/0.2875842775118721

        # add the dataframe to the plot
        ax.plot(data['t'], data['density'], label=label)

        # we only want to fit the data for the interval (1, 1000)
        for i in data['t']:
            if i > 100:
                # get index of i
                index = data['t'].tolist().index(i)
                t = np.log(data['t'][index:])
                rho = np.log(data['density'][index:])
                break

        # do a linear fit
        slope, intercept, r_value, p_value, std_err = stats.linregress(t, rho)
        # calculate the r squared value
        r_squared = r_value**2
        # if the r squared value is better than the previous one, save the values
        if r_squared > best_r_squared:
            best_r_squared = r_squared
            best_alpha = slope
            best_b = intercept
            critical_lambda = infection_rate

        # save the values and the lambda
        fit_list.append([slope, intercept, r_squared, infection_rate])
        
    # create linespace for x values
    x = np.linspace(-1e2, 1e2, 1000)

    alpha = best_alpha
    b = best_b
    y = alpha*x+b
    x_exp = np.exp(x)
    y_exp = np.exp(y)

    # print each fit in the terminal
    print("Fits:")
    for fit in fit_list:
        print(f"alpha: {fit[0]} with r squared: {fit[2]} and b: {fit[1]} for lambda: {fit[3]}")
    
    # plot the best fit in black
    label = f"linear fit"
    # ax.plot(x_exp, y_exp, color='black', label=label)
    print(f"best alpha: {best_alpha} with r squared: {best_r_squared} and b: {best_b} for lambda: {critical_lambda}")

    configure_plot(ax)

    #show the plot
    plt.show()

if __name__ == '__main__':
    plotter()
