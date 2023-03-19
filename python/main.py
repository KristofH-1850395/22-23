# Main class, execute from here
import system as sys
import matplotlib.pyplot as plt
import random
import csv
import bisect

def main():
    find_critical_exponent()
    
def find_critical_exponent():
    z = 3.29785 # expected critical exponent
    T = int(10**3) # simulation time
    l = 2 # infection rate
    data_dict = {}

    I = 1000  #ensemble size
    # create ensemble
    for i in range(I):
        print(f"running simulation {i + 1} of {I}")

        t = 0
        system = sys.System(T, z, l)
        data = []
        mc_duration = 1 / (system.N * (1 + l))

        # initial meassurement
        system.calculate_density()
        data.append([t,system.density])

        while t <= T:
            mc_step(system)
            t += mc_duration

            system.calculate_density()
            data.append([t,system.density])

            if system.particle_count == 0:
                break

        data_dict[i] = data
    
    averaged_data = interpolate_data(data_dict, T, I)
    plot_data(averaged_data)
    #save_data(averaged_data, l)

def mc_step(sys):
    # The MC step will consist of choosing a randon position x, picking annihilation or creation at random, and attempting to perform the selected process

    lat = sys.lattice
    x = random.choice(range(len(lat)))
    system_random = random.SystemRandom()
    r = system_random.random() # random number between 0 and 1
    
    # select creation if r <= sys.v
    if r <= sys.v:
        # now we pick a random neighbour
        d = random.choice([-1, 1])

        # periodic boundary conditions
        # y = (x + d) % len(lat)
        y = x + d
        if y == -1:
            y = len(lat) - 1
        elif y == len(lat):
            y = 0

        sys.create(x,y)
    else:
        sys.annihilate(x)
        
def plot_data(data):
    x_data = list(data.keys())

    y_data = []
    for x in x_data:
        y_data.append(data[x])

    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.scatter(x_data, y_data, s=1)
    ax.set_xscale('log')
    ax.set_yscale('log')    
    ax.set_ylim([10**-10 , 10**0])
    ax.set_xlim([10**-10 , 10**5])
    plt.show()

def interpolate_data(data_dict, T, I):
    delta_t = T / 10**4
    n_interations = I
    simulation_time = T
    average_data = {}
    
    for data in data_dict.values():
        t_data = [x[0] for x in data]
        y_data = [x[1] for x in data]

        N = 0
        while N * delta_t < simulation_time:
            curr_t = N * delta_t
            index = bisect.bisect(t_data, curr_t)

            if curr_t not in average_data.keys():
                average_data[curr_t] = y_data[index - 1] / n_interations
            else:
                average_data[curr_t] += y_data[index - 1] / n_interations

            N += 1

    myKeys = list(average_data.keys())
    myKeys.sort()
    sorted_dict = {i: average_data[i] for i in myKeys}
    
    return sorted_dict

def save_data(data, parameter):
    # specify the file path and name
    filename = f"data/simulation_lambda_{parameter}.csv"

    # open the file in write mode
    with open(filename, mode='w', newline='') as file:
        # create a csv writer object
        writer = csv.writer(file)

        # write the header
        writer.writerow(["t", "density"])

        # write the data
        for t in data.keys():
            writer.writerow([t, data[t]])

if __name__ == "__main__":
    main()