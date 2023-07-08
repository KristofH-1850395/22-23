#include "../include/bachelorProcess.h"

// constructor
ContactProcess::ContactProcess(float infectionRate, int systemSize) {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->infectionRate = infectionRate;
    this->density = 2; // one A particle per site
    this->creationProbability = 4 * infectionRate / (1 + 12 * infectionRate);
    this->mixingProbability = 8 * infectionRate / (1 + 12 * infectionRate);
    this->latticeSize = systemSize;
    this->particleCountA = latticeSize; // creating a homogeneous lattice
    this->particleCountB = 0;
    for (int i = 0; i < latticeSize; i++) {
        lattice.push_back('A');
    }
}

void ContactProcess::create(int x, int y) {
    // create an A particle if A or B neighbours a vacant site
    if ((this->lattice[x] == 'A' || this->lattice[x] == 'B') && this->lattice[y] == '0') {
        this->lattice[y] = 'A';
        this->particleCountA++;
    }
    else if (this->lattice[x] == '0' && (this->lattice[y] == 'A' || this->lattice[y] == 'B')) {
        this->lattice[x] = 'A';
        this->particleCountA++;
    }
    calculateDensity();
}

void ContactProcess::annihilate(int x) {
    if (this->lattice[x] == 'A') {
        this->lattice[x] = '0';
        this->particleCountA--;
    }
    calculateDensity();
}

void ContactProcess::mix(int x, int y) {
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
    } else if (this->lattice[x] == 'B' && this->lattice[y] == 'B') {
        this->lattice[x] = 'A';
        this->lattice[y] = 'A';
        this->particleCountA += 2;
        this->particleCountB -= 2;
    }
    calculateDensity();
}

void ContactProcess::calculateDensity() {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->density = ((float)this->particleCountA * 2 + (float)this->particleCountB) / (float)this->latticeSize;
}