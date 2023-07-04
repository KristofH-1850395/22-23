#this file will plot all the data in the data folder in a scaled log log plot
import os
import pandas as pd
import matplotlib.pyplot as plt

def scale_plotter():
    # defining parameters
    alpha = 0.15947
    lambda_critical = 3.29785
    nu_parallel = 1.73383 #this is our guess

     # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, 'data')

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
        x_axis =  []
        for t in data['t']:
            x_axis.append(t * (simulated_lambda - lambda_critical)**nu_parallel)

        y_axis = []
        for density in data['density']:
            y_axis.append(density * (t ** alpha))

        # calculate delta_lambda
        delta_lambda = round(simulated_lambda - lambda_critical, 4)
        #determine which multiple of delta_lambda it is
        multiple = int(delta_lambda/0.0128)
        #label the plot with the multiple
        plot_label = str(multiple) + ' * 0.0128'

        #determine color of the plot
        if delta_lambda < 0:
            color = 'r'
        elif delta_lambda > 0:
            color = 'g'
        else:
            color = 'b'
        
        # add the dataframe to the plot
        plt.plot(x_axis, y_axis, label=plot_label, color=color)

    # Plot the data
    plt.xlabel('t * (lambda - lambda_critical)^nu_parallel')
    plt.ylabel('density * t^alpha')
    plt.title('All CSV Data')

    #set the axis to log scale
    plt.xscale('log')
    plt.xlim(1e-2, 1e2)
    plt.yscale('log')
    plt.ylim(1e-1, 1e1)

    #add a legend
    plt.legend()

    #show the plot
    plt.show()


if __name__ == '__main__':
    scale_plotter()