import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def scale_plotter(z, ax):
    alpha = 0.16

    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data
    dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling

    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # create an empty DataFrame to store all the data
        data = pd.DataFrame()

        # define size from file name
        m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        size = int(m.group(2))

        # read the csv file
        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        # convert data to tuple
        data = data.to_numpy()
        x_axis = []
        y_axis = []

        # loop through the data and scale it
        for i in range(len(data)):
            t = data[i][0]
            density = data[i][1]            

            if t == 0:
                continue

            x_axis.append(t / size**z)
            y_axis.append(density * (t ** alpha))
        
        # add the dataframe to the plot
        ax.plot(x_axis, y_axis, label=f"L={size}")

    # Set label and title
    ax.set_xlabel(r'$\frac{t}{L^z}$')
    ax.set_ylabel(r'$\rho(t) t^\alpha$')
    ax.set_title('Finite Size Scaling')
    
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    # set the axis to log scale
    ax.set_xscale('log')
    ax.set_xlim(1e-4, 1e1)
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 1e0)

    # add a legend
    ax.legend()

    # sort both labels and handles by labels
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles, labels)

    # show the plot
    plt.show()

if __name__ == '__main__':
    # defining parameter
    z = 1.58 #this is our guess

    # create the figure and the axes
    fig, ax = plt.subplots()
    gs = GridSpec(6, 5, figure=fig)

    # create the text box and the button
    left, bottom, width, height = 0.125, 0.0125, 0.04, 0.02
    axbox_text_z = fig.add_axes([left, bottom, width, height])
    text_box_z = TextBox(axbox_text_z, "z:   ")
    text_box_z.set_val(z)

    left, bottom, width, height = 0.17, 0.0125, 0.1, 0.02
    axbox_button = fig.add_axes([left, bottom, width, height])
    button = Button(axbox_button, "Update")

    # define the function that will be called when the button is pressed
    def submit(expression):
        if expression.inaxes == axbox_button: # Make sure the button was pressed
            ax.lines.clear()
            scale_plotter(float(text_box_z.text), ax)

    # connect the button event with the function submit
    text_box_z.disconnect(text_box_z.disconnect_events) # Disconnect all other events
    text_box_z.connect_event('button_press_event', submit) # Connect the button event

    scale_plotter(z, ax)