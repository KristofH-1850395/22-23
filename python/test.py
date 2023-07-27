import os
import re
import pandas as pd
from scipy.optimize import minimize
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

# create class for data
class DataSet:
    def __init__(self, delta, data):
        self.delta = delta
        self.data = data

# create global variables
data = []
critical_lambda = 3.29785
initial_guess = [0.16, 1.7]

def initialisation():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data for CP
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output/') # regular data for BP

    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling    

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(dir_path, csv_file)
        df = pd.read_csv(csv_path)

        # get the lattice length from the file name
        match = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)

        # calculate the delta
        curr_lambda = float(match.group(1))
        delta = curr_lambda - critical_lambda

        # ignore the data from the critical point (has no contribution)
        if delta == 0:
            continue
        
        ds = DataSet(delta, df)
        data.append(ds)

def interpolation_function(x, reference_data):
    # if x is in the range of the reference data
    if x < reference_data[0][0] or x > reference_data[-1][0]:
        return np.nan

    func = interpolate.CubicSpline(reference_data[:,0], reference_data[:,1], extrapolate=False)

    return func(x)


def calculate_estimated_residuals(initial_guess):
    alpha = initial_guess[0]
    nu = initial_guess[1]

    sum_residuals = 0
    N_over = 0

    # loop over all data sets
    for p in data:
        # get the delta and the data
        df = p.data

        # convert the dataframe to a numpy array
        reference_data = df.to_numpy()

        print(f"Calculating for delta = {p.delta}...", end="\r")

        # loop over every other data set
        for j in data:
            if j == p:
                continue
        
            # get the delta and the data
            delta_j = round(j.delta, 4)
            df = j.data

            # convert the dataframe to a numpy array
            working_data = df.to_numpy()

            # loop over all the rows in the data
            for i in range(len(working_data)):
                # calculate the terms from the tabulated data
                t = working_data[i][0]
                rho = working_data[i][1]

                # calculate the terms from the working data
                left_term = (t**alpha) * rho
                right_term = interpolation_function((t**(-1/nu)) * delta_j**(-1), reference_data)

                if np.isnan(right_term):
                    continue

                N_over += 1
                sum_residuals += (left_term - right_term)

    if N_over == 0:
        return 1000
    
    sum_residuals = sum_residuals / N_over

    # print the sum of the residuals and overwite the previous line
    print(f"Sum of residuals: {sum_residuals} for alpha = {alpha} and nu = {nu}", end="\r")

    return sum_residuals

def main():
    # initialise the data
    initialisation()
    
    calculate_estimated_residuals(initial_guess)
    print()

    # print("=== MINIMISING ===")
    # result = minimize(calculate_estimated_residuals, initial_guess, method='Nelder-Mead')
    # print()
    # print(result)


if __name__ == "__main__":
    main()