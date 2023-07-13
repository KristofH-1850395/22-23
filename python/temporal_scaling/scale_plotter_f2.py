import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def scale_plotter(lambda_critical, alpha, nu_parallel, ax):
    # defining parameters

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

            if t < 2:
                continue

            x_axis.append(t * abs(simulated_lambda - lambda_critical)**nu_parallel)
            y_axis.append(density * (t ** alpha))

        # calculate delta_lambda
        delta_lambda = round(simulated_lambda - lambda_critical, 4)
        #determine which multiple of delta_lambda it is
        multiple = int(delta_lambda/0.0128)
        #label the plot with the multiple
        plot_label = str(multiple) + ' * 0.0128'

        #determine color of the plot
        if delta_lambda < 0:
            color = '#a31621'
        elif delta_lambda > 0:
            color = '#4e8098'
        else:
            color = 'b'
        
        # add the dataframe to the plot
        ax.plot(x_axis, y_axis, label=plot_label, color=color)

    # set the labels and title of the plot
    ax.set_xlabel(r'$t \Delta^{\nu_{//}}$')
    ax.set_ylabel(r'$\rho(t) t^\alpha$')
    ax.set_title('Scaling Relation of the Density')

    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    #set the axis to log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    #add a legend to ax
    ax.legend()

    # sort both labels and handles by labels
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles, labels)

    #show the plot
    plt.show()


if __name__ == '__main__':
    # defining parameters
    alpha = 0.216
    nu_parallel = 2.4  # this is our guess
    lambda_critical = 0.32939

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