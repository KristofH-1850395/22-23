# DEPRECATED

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def scale_plotter(lambda_critical, alpha, nu_parallel, ax):
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data for CP
    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    dir_path = os.path.join(root_path, 'data/bachelor_process/output') # regular data for BP
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling


    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # create an empty DataFrame to store all the data
        data = pd.DataFrame()

        # define lambda from file name
        m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        simulated_lambda = float(m.group(1))

        if simulated_lambda - lambda_critical == 0:
            continue

        # read the csv file
        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #convert  data to tuple
        data = data.to_numpy()
        x_axis = []
        y_axis = []

        #loop through the data and scale it
        for i in range(len(data)):
            t = data[i][0]
            density = data[i][1]            

            if t < 10:
                continue

            x_axis.append(t**(1/nu_parallel) * (simulated_lambda - lambda_critical))
            y_axis.append(density * (t ** alpha))

        # calculate delta_lambda
        delta_lambda = round(simulated_lambda - lambda_critical, 4)
        #determine which multiple of delta_lambda it is
        multiple = int(delta_lambda/0.0128)
        #label the plot with the multiple
        delta = str(multiple) + ' * 0.0128'
        plot_label = r"$\Delta = $" + str(delta)
        
        # add the dataframe to the plot
        ax.plot(x_axis, y_axis, label=plot_label)

    # set the labels and title
    ax.set_xlabel(r'$t^{1/\nu_{//}} \Delta$')
    ax.set_ylabel(r'$\rho(t) t^\alpha$')
    ax.set_title('Scaling Relation of the Density')

    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    #set the axis to log scale
    ax.set_xscale('linear')
    ax.set_yscale('linear')

    # auto scale the axis
    ax.autoscale()

    #add a legend
    ax.legend()

    #show the plot
    plt.show()


if __name__ == '__main__':
    # defining parameters
    alpha = 0.232 # from log plotter
    nu_parallel = 2.5  # this is our guess
    lambda_critical = 0.65768 # from log plotter

    #create the figure and the axes
    fig, ax = plt.subplots()
    gs = GridSpec(6, 5, figure=fig)

    #create the text box and the button    
    left, bottom, width, height = 0.125, 0.035, 0.04, 0.025
    axbox_text_alpha = fig.add_axes([left, bottom, width, height])
    text_box_alpha = TextBox(axbox_text_alpha, "alpha:   ")
    text_box_alpha.set_val(alpha)

    left, bottom, width, height = 0.125, 0.005, 0.04, 0.025
    axbox_text_nu_parallel = fig.add_axes([left, bottom, width, height])
    text_box_nu_parallel = TextBox(axbox_text_nu_parallel, "nu_parallel:   ")
    text_box_nu_parallel.set_val(nu_parallel)

    left, bottom, width, height = 0.17, 0.005, 0.1, 0.055
    axbox_button = fig.add_axes([left, bottom, width, height])
    button = Button(axbox_button, "Update")

    #define the function that will be called when the button is pressed
    def submit(expression):
        if expression.inaxes == axbox_button: # Make sure the button was pressed
            ax.lines.clear()
            scale_plotter(lambda_critical, float(text_box_alpha.text), float(text_box_nu_parallel.text), ax)

    # Connect the button event with the function submit
    text_box_alpha.disconnect(text_box_alpha.disconnect_events) # Disconnect all other events
    text_box_alpha.connect_event('button_press_event', submit) # Connect the button event

    text_box_nu_parallel.disconnect(text_box_nu_parallel.disconnect_events) # Disconnect all other events
    text_box_nu_parallel.connect_event('button_press_event', submit) # Connect the button event
    
    scale_plotter(lambda_critical, alpha, nu_parallel, ax)