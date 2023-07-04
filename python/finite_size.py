import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def scale_plotter(z, ax):
    alpha = 0.15947

    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.path.join(root_path, 'data/finite_size')

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # create an empty DataFrame to store all the data
        data = pd.DataFrame()

        # define size from file name
        size = int(csv_file[-6:-4])

        # read the csv file
        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #convert data to tuple
        data = data.to_numpy()
        x_axis = []
        y_axis = []

        #loop through the data and scale it
        for i in range(len(data)):
            t = data[i][0]
            density = data[i][1]            

            if t == 0:
                continue

            x_axis.append(t / size**z)
            y_axis.append(density * (t ** alpha))
        
        # add the dataframe to the plot
        ax.plot(x_axis, y_axis, label=size)

    # Plot the data
    ax.set_xlabel('t / L**z')
    ax.set_ylabel('rho * (t ** alpha)')
    ax.set_title('All CSV Data')

    #set the axis to log scale
    ax.set_xscale('log')
    ax.set_xlim(1e-3, 1e1)
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 1e0)

    #add a legend
    ax.legend()

    #show the plot
    plt.show()

if __name__ == '__main__':
    # defining parameter
    z = 1.58 #this is our guess

    #create the figure and the axes
    fig, ax = plt.subplots()
    gs = GridSpec(6, 5, figure=fig)

    #create the text box and the button
    left, bottom, width, height = 0.125, 0.0125, 0.04, 0.02
    axbox_text_z = fig.add_axes([left, bottom, width, height])
    text_box_z = TextBox(axbox_text_z, "z:   ")
    text_box_z.set_val(z)

    left, bottom, width, height = 0.17, 0.0125, 0.1, 0.02
    axbox_button = fig.add_axes([left, bottom, width, height])
    button = Button(axbox_button, "Update")

    #define the function that will be called when the button is pressed
    def submit(expression):
        if expression.inaxes == axbox_button: # Make sure the button was pressed
            ax.lines.clear()
            scale_plotter(float(text_box_z.text), ax)

    # Connect the button event with the function submit
    text_box_z.disconnect(text_box_z.disconnect_events) # Disconnect all other events
    text_box_z.connect_event('button_press_event', submit) # Connect the button event

    scale_plotter(z, ax)