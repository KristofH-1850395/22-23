#include "../../include/bachelorProcess.h"
#include "math.h"

BachelorProcess::BachelorProcess(float infectionRate, int systemSize) {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->infectionRate = infectionRate;
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

void BachelorProcess::create(int x, int y) {
    // create an A particle if A or B neighbours a vacant site
    if ((this->lattice[x] == 'A' || this->lattice[x] == 'B') && this->lattice[y] == '0') {
        this->lattice[y] = 'A';
        this->particleCountA++;
    }

    updateDensity();
}

void BachelorProcess::annihilate(int x) {
    if (this->lattice[x] == 'A') {
        this->lattice[x] = '0';
        this->particleCountA--;
    }

    updateDensity();
}

void BachelorProcess::mix(int x, int y) {
    if (this->lattice[x] == 'A' && this->lattice[y] == 'B') {
        this->lattice[x] = 'B';
        this->lattice[y] = 'A';
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

    updateDensity();
}

void BachelorProcess::updateDensity() {
    // note for the reader: one A particle is equivalent to two B particles, as such we have density between 0 and 2
    this->density = (((float)this->particleCountA * 2) + (float)this->particleCountB) / (float)this->latticeSize;
}

void BachelorProcess::monteCarloStep() {
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