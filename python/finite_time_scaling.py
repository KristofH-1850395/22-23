# =======================================================================
# ===Script for calculating the exponents alpha and nu_//================
# ===We use a scaling relation valid for small t and large L=============
# ===will also plot the relation with the determined exponents===========
# =======================================================================

import os
import re
import pandas as pd
from scipy.optimize import minimize
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(['science', 'ieee', 'no-latex'])
plt.rcParams.update({'figure.dpi': '300'})

# create class for data
class DataSet:
    def __init__(self, delta, data): 
        self.delta = delta
        self.data = data

# create global variables
data = []

# ==== CP ====
# initial_guess = [1.6, 0.159] # nu_par, alpha
# path_to_data = 'data/contact_process/output'
# lambda_critical = 3.29785 # from literature
# 
# ==== BP ====  
initial_guess = [3.22, 0.29] # [nu_par, alpha]
path_to_data = 'data/bachelor_process/test'
lambda_critical = 0.63

def initialisation():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    dir_path = os.path.join(root_path, path_to_data)

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(dir_path, csv_file)
        df = pd.read_csv(csv_path)

        # get the delta from the file name
        match = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        current_lambda = float(match.group(1))
        delta = round(current_lambda - lambda_critical, 4)

        if delta == 0:
            continue
        
        ds = DataSet(delta, df)
        data.append(ds)

def trim_data(df):
    # trim the data for low t
    df = df[df['t'] > 100]

    # trim the data if the density is low
    df = df[df['density'] > 0.0001]

    return df

def scale_data(data, delta, nu_par, alpha):
    x_axis = []
    y_axis = []

    for i in range(len(data)):
        t = data[i][0]
        density = data[i][1]

        x_axis.append((t ** (1/nu_par)) * delta)
        y_axis.append(density * (t ** alpha))

    return x_axis, y_axis

# returns the interpolation function and the x-axis limits
# def calculate_interpolation_function(data, delta, c, d):
def calculate_interpolation_function(data, delta, nu_par, alpha):
    # scale the data
    x_axis, y_axis = scale_data(data, delta, nu_par, alpha)

    if delta < 0:
        # reverse x_axis and y_axis
        x_axis = x_axis[::-1]
        y_axis = y_axis[::-1]

    # create interpolation function
    f = interpolate.CubicSpline(x_axis, y_axis, extrapolate=None)

    return f, [x_axis[0], x_axis[-1]]

# calculate the residuals for the given parameters
def calculate_estimated_residuals(initial_guess):
    c = initial_guess[0] 
    d = initial_guess[1] 

    sum_residuals = 0
    N_over = 0

    # loop through all the data sets
    for p in data:
        # get lattice length and dataset
        delta_p, data_p = p.delta, p.data.to_numpy()
        f, [x_min, x_max] = calculate_interpolation_function(data_p, delta_p, c, d)

        # loop through all the other data sets
        for j in data:
            # get lattice length and dataset
            delta_j = j.delta

            # ignore the same data set
            if delta_j == delta_p:
                continue

            data_j = trim_data(j.data).to_numpy()

            # scale the data
            x_j, y_j = scale_data(data_j, delta_j, c, d)

            # loop through all the points
            for i in range(len(x_j)):
                x_ij = x_j[i]
                y_ij = y_j[i]

                # ignore points outside the interpolation range
                if x_ij < x_min or x_ij > x_max:
                    continue

                # calculate the residual
                sum_residuals += abs(y_ij - f(x_ij)) / (y_ij + f(x_ij))
                N_over += 1

    if N_over == 0:
        return 99 # randomly chosen error code, if no overlapping pairs then we should reject the parameters

    return sum_residuals / N_over

def report_progress(x):
    c = x[0]
    d = x[1]

    print(f"current c: {c} and d: {d}")

def determine_error(optimal_parameters):
    width = 0.01
    c_0 = optimal_parameters[0]
    d_0 = optimal_parameters[1]
    
    norm = calculate_estimated_residuals([c_0, d_0])
    
    delta_c = width * c_0 * (2 * np.log(calculate_estimated_residuals([c_0 * (1 + width), d_0]) / norm))**(-1/2)
    delta_d = width * d_0 * (2 * np.log(calculate_estimated_residuals([c_0, d_0 * (1 + width)]) / norm))**(-1/2)

    return delta_c, delta_d

def plot_data(data, best_c, best_d):
    # loop through all the data sets
    for p in data:
        # get lattice length and dataset
        delta, data_set = p.delta, trim_data(p.data).to_numpy()

        # scale the data
        x_axis, y_axis = scale_data(data_set, delta, best_c, best_d)

        # plot the data
        # determine which multiple of delta_lambda it is
        multiple = int(round(delta/0.0128, 0))
        if multiple > 0:
            plt.plot(x_axis, y_axis, label=fr"$ \lambda_c + {multiple} \delta$")
        else:
            plt.plot(x_axis, y_axis, label=fr"$ \lambda_c {multiple} \delta$")

    # Set label and title
    plt.xlabel(r'$t^{1/\nu_{//}} \Delta$')
    plt.ylabel(r'$\rho(t) t^\alpha$')
    
    # sort both labels and handles by labels
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    plt.legend(handles, labels)

    plt.show()

def main():
    # initialise the data
    initialisation()

    # minimise the residuals
    result = minimize(calculate_estimated_residuals, initial_guess, method='Nelder-Mead', callback=report_progress)
    c_0 = result.x[0]
    d_0 = result.x[1]

    # determine the error
    delta_c, delta_d = determine_error([c_0, d_0])

    # print the results
    print("=== RESULTS ===")
    print(f"alpha = {d_0} +/- {delta_d}")
    print(f"nu_par = {c_0} +/- {delta_c}")
    print("===============")

    plot_data(data, c_0, d_0)

if __name__ == "__main__":
    main()