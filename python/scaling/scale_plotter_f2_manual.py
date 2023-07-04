#this file will plot all the data in the data folder in a scaled log log plot
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def scale_plotter(lambda_critical, alpha, nu_parallel, ax):
    # defining parameters

     # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

        #convert  data to tuple
        data = data.to_numpy()
        x_axis = []
        y_axis = []

        #loop through the data and scale it
        for i in range(len(data)):
            t = data[i][0]
            density = data[i][1]

            if t == 0:
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
            color = 'r'
        elif delta_lambda > 0:
            color = 'g'
        else:
            color = 'b'
        
        # add the dataframe to the plot
        ax.plot(x_axis, y_axis, label=plot_label, color=color)

    # Plot the data
    ax.set_xlabel('t * (lambda - lambda_critical)^nu_parallel')
    ax.set_ylabel('density * t^alpha')
    ax.set_title('All CSV Data')

    #set the axis to log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    #add a legend to ax
    ax.legend()

    #show the plot
    plt.show()


if __name__ == '__main__':
    # defining parameters
    alpha = 0.15947
    nu_parallel = 1.73383 #this is our guess
    lambda_critical = 3.29785

    #create the figure and the axes
    fig, ax = plt.subplots()
    gs = GridSpec(6, 5, figure=fig)

    #create the text box and the button
    axbox_text_alpha = fig.add_axes([0.1, 0.05, 0.5, 0.025])
    text_box_alpha = TextBox(axbox_text_alpha, "alpha")
    text_box_alpha.set_val(alpha)

    axbox_text_nu_parallel = fig.add_axes([0.1, 0.01, 0.5, 0.025])
    text_box_nu_parallel = TextBox(axbox_text_nu_parallel, "nu_parallel")
    text_box_nu_parallel.set_val(nu_parallel)

    axbox_button = fig.add_axes([0.65, 0.01, 0.1, 0.075])
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