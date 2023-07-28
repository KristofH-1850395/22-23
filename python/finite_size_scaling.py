# =======================================================================
# ===Script for calculating the exponents alpha and nu_perpandicular=====
# ===We use a finite size scaling in the critical point==================
# ===will also plot the relation with the determined exponents===========
# =======================================================================

import os
import re
import pandas as pd
from scipy.optimize import minimize
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

# create class for data
class DataSet:
    def __init__(self, lattice_length, data):
        self.lattice_length = lattice_length
        self.data = data

# create global variables
data = []

# ==== CP ====
# initial_guess = [1.58, -0.2528] # [c, d] = [z, -alpha * z] --- from literature
# path_to_data = 'data/contact_process/output_finite'
#
# ==== BP ====
initial_guess = [1.7363122606649988, -0.39678649038612845] # [c, d] = [z, -alpha * z]
path_to_data = 'data/bachelor_process/output_finite'

def initialisation():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, path_to_data)

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(dir_path, csv_file)
        df = pd.read_csv(csv_path)

        # get the lattice length from the file name
        match = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        lattice_length = int(match.group(2))
        
        ds = DataSet(lattice_length, df)
        data.append(ds)

def trim_data(df):
    # trim the data for low t
    df = df[df['t'] > 10]

    # trim the data if the density is zero
    df = df[df['density'] > 0.01]

    return df

def scale_data(data, L, c, d):
    x_axis = []
    y_axis = []

    for i in range(len(data)):
        t = data[i][0]
        density = data[i][1]

        x_axis.append(t * (L**-c))
        y_axis.append(density * (L ** -d))

    return x_axis, y_axis

# returns the interpolation function and the x-axis limits
def calculate_interpolation_function(data, L, c, d):
    # scale the data
    x_axis, y_axis = scale_data(data, L, c, d)

    # create interpolation function
    f = interpolate.CubicSpline(x_axis, y_axis, extrapolate=None)

    return f, [x_axis[0], x_axis[-1]]

# calculate the residuals for the given parameters
def calculate_estimated_residuals(initial_guess):
    c = initial_guess[0] # c = z
    d = initial_guess[1] # d = - alpha * z

    sum_residuals = 0
    N_over = 0

    # loop through all the data sets
    for p in data:
        # get lattice length and dataset
        L_p, data_p = p.lattice_length, p.data.to_numpy()
        f, [x_min, x_max] = calculate_interpolation_function(data_p, L_p, c, d)

        # loop through all the other data sets
        for j in data:

            # get lattice length and dataset
            L_j = j.lattice_length

            # ignore the same data set
            if L_j == L_p:
                continue

            data_j = trim_data(j.data).to_numpy()

            # scale the data
            x_j, y_j = scale_data(data_j, L_j, c, d)

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
    
    # print the sum of the residuals
    print(f"sum of residuals: {sum_residuals / N_over} for c={c} and d={d}", end="\r")

    return sum_residuals / N_over

# callback function for the minimisation
def report_progress(x):
    c = x[0]
    d = x[1]

    print(f"current c: {c} and d: {d}")

def determine_error(optimal_parameters):
    width = 0.01
    c_0 = optimal_parameters[0]
    d_0 = optimal_parameters[1]

    c_bounds = calculate_estimated_residuals([c_0 - width * c_0, d_0]), calculate_estimated_residuals([c_0 + width * c_0, d_0])
    d_bounds = calculate_estimated_residuals([c_0, d_0 - width * d_0]), calculate_estimated_residuals([c_0, d_0 + width * d_0])
    norm = calculate_estimated_residuals([c_0, d_0])

    c_lower, c_upper = np.sqrt(2 * np.log(c_bounds[0] / norm)), np.sqrt(2 * np.log(c_bounds[1] / norm))
    d_lower, d_upper = np.sqrt(2 * np.log(d_bounds[0] / norm)), np.sqrt(2 * np.log(d_bounds[1] / norm))

    delta_c = width * c_0 * abs(c_upper - c_lower)
    delta_d = width * d_0 * abs(d_upper - d_lower)

    return delta_c, delta_d

def plot_data(data, best_c, best_d):
    # loop through all the data sets
    for p in data:
        # get lattice length and dataset
        L, data_set = p.lattice_length, trim_data(p.data).to_numpy()

        # scale the data
        x_axis, y_axis = scale_data(data_set, L, best_c, best_d)

        # plot the data
        plt.plot(x_axis, y_axis, label=f"L={L}")

    # determine exponents so we can show them in the title
    z = round(best_c, 2)
    alpha = round(-best_d / best_c, 2)

    # Set label and title
    plt.xlabel(r'$L^{-z} t$', size=20)
    plt.ylabel(r'$L^{\alpha z} \rho(t) $', size=20)
    plt.title(rf'Finite Size Scaling: $\alpha = {alpha}$, $z = {z}$', size=30)    
    plt.tick_params(axis='both', which='major', labelsize=12)

    # set the axis to log scale
    plt.xscale('log')
    plt.yscale('log')
    
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
    print(f"z = {c_0} +- {delta_c}")
    print(f"alpha = {-d_0 / c_0} +- {delta_d / c_0}")
    print("===============")

    plot_data(data, c_0, d_0)

if __name__ == "__main__":
    main()