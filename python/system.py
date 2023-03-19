import numpy as np

class System:
    # This is the lattice class. It holds all the relevant properties pertaining to the system, it does not hold properties pertaining to simulation settings

    def __init__(self, sim_time, expected_exponent, infection_rate):    
        self.STD_SIZE = 10**2 # standard size of lattice
        self.l = infection_rate # infection rate lambda
        self.v = self.l / (1 + self.l) # creation probability
        #self.N_min = int(np.ceil(sim_time ** (1/expected_exponent))) # length of 
        self.N_min = 0
        
        self.N = 0
        if self.STD_SIZE < self.N_min:
            self.N = self.N_min
        else:
            self.N = self.STD_SIZE

        self.lattice = np.ones(self.N, int)
        self.particle_count = self.N
        self.density = 1

    def create(self, x, y):
        if self.lattice[x] == 1 and self.lattice[y] == 0:
            self.lattice[y] = 1
            self.particle_count += 1

    def annihilate(self, x):
        if self.lattice[x] == 1:
            self.lattice[x] = 0
            self.particle_count += -1
        
    def calculate_density(self):
        self.density = self.particle_count / self.N
