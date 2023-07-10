#this file will plot all the data in the data folder in a log log plot
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox, Button
from matplotlib.gridspec import GridSpec

def plotter(alpha, b, ax):
    # get the path of the data folder
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # dir_path = os.path.join(root_path, 'data/contact_process/output') # regular data for CP
    # dir_path = os.path.join(root_path, 'data/contact_process/output_finite') # for finite size scaling
    dir_path = os.path.join(root_path, 'data/bachelor_process/output') # regular data for BP
    # dir_path = os.path.join(root_path, 'data/bachelor_process/output_finite') # for finite size scaling


    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Loop through all the CSV files and append the data to the DataFrame
    for csv_file in csv_files:        
        # Create an empty DataFrame to store all the data
        data = pd.DataFrame()

        csv_path = os.path.join(dir_path, csv_file)
        data = pd.read_csv(csv_path)

        #get label from file name
        m = re.search("lambda_([\d\.]+)_size_(\d+)\.csv", csv_file)
        label = r'$\lambda = $' + m.group(1)

        # add the dataframe to the plot
        ax.plot(data['t'], data['density'], label=label)


    # create linespace for x values
    x = np.linspace(0, 1e2, 1000)
    # calculate y values
    y = -alpha*x+b
    x_exp = np.exp(x)
    y_exp = np.exp(y)
    # plot the line in black
    label = f"y = -{alpha}x + {b}"
    ax.plot(x_exp, y_exp, color='black', label=label)


    # Plot the data
    ax.set_xlabel('t')
    ax.set_ylabel(r'$\rho(t)$')
    ax.set_title('Density of the system as a function of time')

    #set the size of the labels
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    plt.legend(fontsize=16)

    #set the axis to log scale
    ax.set_xscale('log')
    ax.set_xlim(1, 1e2)
    ax.set_yscale('log')
    ax.set_ylim(2e-1, 1e0)

    #add a legend
    ax.legend()

    #show the plot
    plt.show()

if __name__ == '__main__':
# defining parameters
    alpha = 0.179 # this is our guess
    b = -0.2 

    #create the figure and the axes
    fig, ax = plt.subplots()
    gs = GridSpec(6, 5, figure=fig)

    #create the text box and the button  
    left, bottom, width, height = 0.125, 0.035, 0.04, 0.025
    axbox_text_alpha = fig.add_axes([left, bottom, width, height])
    text_box_alpha = TextBox(axbox_text_alpha, "alpha:   ")
    text_box_alpha.set_val(alpha)

    left, bottom, width, height = 0.125, 0.005, 0.04, 0.025
    axbox_text_b = fig.add_axes([left, bottom, width, height])
    text_box_b = TextBox(axbox_text_b, "b:   ")
    text_box_b.set_val(b)

    left, bottom, width, height = 0.17, 0.005, 0.1, 0.055
    axbox_button = fig.add_axes([left, bottom, width, height])
    button = Button(axbox_button, "Update")

    #define the function that will be called when the button is pressed
    def submit(expression):
        if expression.inaxes == axbox_button: # Make sure the button was pressed
            ax.lines.clear()
            plotter(float(text_box_alpha.text), float(text_box_b.text), ax)

    # Connect the button event with the function submit
    text_box_alpha.disconnect(text_box_alpha.disconnect_events) # Disconnect all other events
    text_box_alpha.connect_event('button_press_event', submit) # Connect the button event

    text_box_b.disconnect(text_box_b.disconnect_events) # Disconnect all other events
    text_box_b.connect_event('button_press_event', submit) # Connect the button event
    
    plotter(alpha, b, ax)
