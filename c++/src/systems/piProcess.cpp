#include "../../include/piProcess.h"
#include "math.h"
#include <iostream>

PiProcess::PiProcess(float infectionRate, int systemSize) {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->contaminationRate = infectionRate;
    this->density = 2; // one A particle per site
    this->normalisation = (1 + (6 * infectionRate));
    this->creationProbability = (2 * infectionRate) / normalisation;
    this->mixingProbability = (4 * infectionRate) / normalisation;
    this->latticeSize = systemSize;
    this->particleCountA = latticeSize; // creating a homogeneous lattice
    this->particleCountB = 0;

    for (int i = 0; i < latticeSize; i++) {
        lattice.push_back('A');
    }
}

void PiProcess::create(int x, int y) {
    // calculate the old number of particles modulo 2
    int old_mod = (this->particleCountA * 2 + this->particleCountB) % 2;

    // create an A particle if A or B neighbours a vacant site
    if ((this->lattice[x] == 'A' || this->lattice[x] == 'B') && this->lattice[y] == '0') {
        this->lattice[y] = 'A';
        this->particleCountA++;
    }

    
    // calculate the new number of particles modulo 2
    int new_mod = (this->particleCountA * 2 + this->particleCountB) % 2;

    //DEBUG:: print the difference between the old and new mod
    if (old_mod != new_mod)
        std::cout << "CREATION EVENT ----- old mod: " << old_mod << " new mod: " << new_mod << std::endl;

    updateDensity();
}

void PiProcess::annihilate(int x) {
    if (this->lattice[x] == 'A') {
        this->lattice[x] = '0';
        this->particleCountA--;
    }

    updateDensity();
}

void PiProcess::mix(int x, int y) {
    // calculate the old number of particles modulo 2
    int old_mod = (this->particleCountA * 2 + this->particleCountB) % 2;

    if (this->lattice[x] == 'A' && this->lattice[y] == 'B') {
        this->lattice[x] = 'B';
        this->lattice[y] = 'A';
    }
    else if (this->lattice[x] == 'B' && this->lattice[y] == 'A') {
        this->lattice[x] = 'A';
        this->lattice[y] = 'B';
    }
    else if (this->lattice[x] == 'A' && this->lattice[y] == 'A') {
        this->lattice[x] = 'B';
        this->lattice[y] = 'B';
        this->particleCountA -= 2;
        this->particleCountB += 2;
    } 
    else if (this->lattice[x] == 'B' && this->lattice[y] == 'B') {
        this->lattice[x] = 'A';
        this->lattice[y] = 'A';
        this->particleCountA += 2;
        this->particleCountB -= 2;
    }

    // calculate the new number of particles modulo 2
    int new_mod = (this->particleCountA * 2 + this->particleCountB) % 2;

    //DEBUG:: print the difference between the old and new mod
    if (old_mod != new_mod)
        std::cout << "MIXING EVENT --- old mod: " << old_mod << " new mod: " << new_mod << std::endl;

    updateDensity();
}

void PiProcess::updateDensity() {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->density = (((float)this->particleCountA * 2) + (float)this->particleCountB) / (float)this->latticeSize;
}

void PiProcess::monteCarloStep() {
    // choose a random index between 0 and latticeSize
    int x = rand() % this->latticeSize;

    // choose a random float between 0 and 1
    float r = (float)rand() / (float)RAND_MAX;

    // attempt to create, mix or annihilate a particle
    if (r <= this->creationProbability) {
        int y = getRandomNeighbour(x);

        // attempt to create a particle
        this->create(x, y);
    } 
    else if (r <= this->creationProbability + this->mixingProbability) {
        int y = getRandomNeighbour(x);

        // attempt to mix a particle
        this->mix(x, y);
    }
    else {
        this->annihilate(x);
    }
}