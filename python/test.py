import os
import re
import pandas as pd
from scipy.optimize import minimize
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

# create class for data
class DataSet:
    def __init__(self, lattice_length, data):
        self.lattice_length = lattice_length
        self.data = data

# create global variables
data = []
# nitial_guess = [1.58, -0.2528] # [c, d] = [z, -alpha * z] --- from literature
initial_guess = [0.5, 0.5]

def initialisation():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # cp
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # bp

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
    df = df[df['t'] > 1]

    # trim the data if the density is zero
    df = df[df['density'] > 0]

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
        L_p = p.lattice_length
        data_p = trim_data(p.data).to_numpy()
        f, [x_min, x_max] = calculate_interpolation_function(data_p, L_p, c, d)
        
        residual = 0
        N = 0

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

            # plot the interpolation function against the data
            x_overlapping = []
            y_overlapping = []

            # loop through all the points
            for i in range(len(x_j)):
                x_ij = x_j[i]
                y_ij = y_j[i]

                # ignore points outside the interpolation range
                if x_ij < x_min or x_ij > x_max:
                    continue

                x_overlapping.append(x_ij)
                y_overlapping.append(y_ij)

                # calculate the residual
                residual += abs(y_ij - f(x_ij)) / (y_ij + f(x_ij))
                N += 1

            # # plot the overlapping data and the overlapping interpolation
            # plt.plot(x_overlapping, y_overlapping, label=f"y_ij")
            # plt.plot(x_overlapping,  f(x_overlapping), label=f"f(x_ij)")

            # plt.xscale('log')
            # plt.yscale('log')
            # plt.legend()
            # plt.show()

            # add the residual to the sum
            sum_residuals += residual
            N_over += N

    if N_over == 0:
        return -99 # randomly chosen error code, if no overlapping pairs then we should reject the parameters
    
    # print the sum of the residuals
    print(f"sum of residuals: {sum_residuals / N_over} for c={c} and d={d}", end="\r")

    return sum_residuals / N_over

def main():
    # initialise the data
    initialisation()

    # minimise the residuals
    result = minimize(calculate_estimated_residuals, initial_guess, method='Nelder-Mead')
    print()
    print(result.x)

if __name__ == "__main__":
    main()