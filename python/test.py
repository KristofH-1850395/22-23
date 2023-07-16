import os
import re
import pandas as pd
from scipy.optimize import minimize
import numpy as np

def get_data_from_csv(data):
    # convert data to tuple
    data = data.to_numpy()
    data_pairs = []

    # loop through the data
    for i in range(len(data)):
        t = data[i][0]
        density = data[i][1]

        data_pairs.append((t, density)) 
    
    return data_pairs

def get_overlapping_interval(data1, data2):
    return 0,0


def plotter():
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling
    print(dir_path)

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    data_list = []

    # Loop through all the CSV files
    for csv_file in csv_files:
        # Create an empty DataFrame to store all the data
        data = pd.DataFrame()

        # read the csv file
        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #get size from file name
        m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        size = int(m.group(2))

        # get the data from the csv
        data_pairs = get_data_from_csv(data)

        # append the data to the list
        data_list.append(size, data_pairs)

if __name__ == "__main__":
    plotter()