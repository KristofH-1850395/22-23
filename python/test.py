import os
import re
import pandas as pd
import sys
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
from scipy import interpolate

# define some global variables
# get the path of the data folder
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling 

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# create a list of lattice lengths
lattice_lengths = []

# convert each file to a list of tuples
data = [] # data[i][j][k] -> i = list, j = pair in list, k = [0,1] -> 0 = t, 1 = density

for csv_file in csv_files:
    csv_path = os.path.join(dir_path, csv_file)
    df = pd.read_csv(csv_path)
    data.append(df.to_numpy())

    # get the lattice length from the file name
    m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
    lattice_lengths.append(int(m.group(2)))   

# define the function to minimize
def func_pb(params):    
    # get the parameters
    c = params[0]
    d = params[1]   
    print(f"trying to minimize with c = {c} and d = {d}")
        
    N = 0
    estimated_residual_sum = 0

    # sum over over each list
    for p in range(len(data)):
        sys.stdout.write(f"\r --- calculating for reference list {p + 1} / {len(data)}")

        # interpolate the data using scipy.interpolate
        t = [data[p][i][0] for i in range(len(data[p]))]
        rho = [data[p][i][1] for i in range(len(data[p]))]
        f = interpolate.interp1d(t, rho, fill_value="extrapolate")
        
        # sum over data[p] every list that isn't data[p]
        for j in range(len(data)):
            if j != p:
                # get the overlapping interval
                start, end = get_overlapping_interval(data[p], data[j])

                # sum over each pair in the overlapping interval
                for i in range(len(data[j])):
                    if data[j][i][0] >= start and data[j][i][0] <= end:
                        N += 1 # calculating N_over
                        
                        t = data[j][i][0] # magic number 0 = t
                        m = data[j][i][1] # magic number 1 = density
                        
                        L = lattice_lengths[j]
                        x = L ** (-c) * t
                        
                        left_term = (L**(-d) * m)
                        rho = f(x)

                        # calculate the error
                        estimated_residual = abs(left_term - rho)

                        #add up all the estimated residuals
                        estimated_residual_sum += estimated_residual

    print() # print a newline

    # calculate the average estimated residual
    average_estimated_residual = estimated_residual_sum / N
    print(f"average estimated residual = {average_estimated_residual}")
    print("==============================================")

    return average_estimated_residual

def get_overlapping_interval(data1, data2):
    # get the lowest t value of the two data sets
    t1_min = data1[0][0]
    t2_min = data2[0][0]
    t_min = max(t1_min, t2_min)

    #get the highest t value of the two data sets
    t1_max = data1[-1][0]
    t2_max = data2[-1][0]
    t_max = min(t1_max, t2_max)

    return t_min, t_max


def main():    
    # minimize func_pb
    initial_guess = [1, 1]

    # minimize with positive bounds
    res = minimize(func_pb, initial_guess, method='L-BFGS-B')
    print(res.x)

    print(f"c = {res.x[0]} =====> eta_p = {1.7 / res.x[0]}")
    print(f"d = {res.x[1]} =====> eta_p = {- 0.16 * 1.7 / res.x[1]}")

if __name__ == "__main__":
    main()