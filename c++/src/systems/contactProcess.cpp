#include "../../include/contactProcess.h"
#include "math.h"

ContactProcess::ContactProcess(float contaminationRate, int systemSize) {
    this->contaminationRate = contaminationRate;
    this->density = 1;
    this->normalisation = (1 + contaminationRate);
    this->creationProbability = contaminationRate / this->normalisation;
    this->latticeSize = systemSize;
    this->particleCount = latticeSize;

    for (int i = 0; i < latticeSize; i++) {
        this->lattice.push_back(1);
    }
}

void ContactProcess::create(int x, int y) {
    if (this->lattice[x] == 1 && this->lattice[y] == 0) {
        this->lattice[y] = 1;
        this->particleCount++;
    }

    updateDensity();
}

void ContactProcess::annihilate(int x) {
    if (this->lattice[x] == 1) {
        this->lattice[x] = 0;
        this->particleCount--;
    }

    updateDensity();
}

void ContactProcess::updateDensity() {
    this->density = (float)this->particleCount / (float)this->latticeSize;
}

void ContactProcess::monteCarloStep() {
    // choose a random index between 0 and latticeSize
    int x = rand() % this->latticeSize;

    // choose a random float between 0 and 1
    float r = (float)rand() / (float)RAND_MAX;

    // attempt to create or annihilate a particle
    if (r <= this->creationProbability) {
        int y = getRandomNeighbour(x);

        // attempt to create a particle
        this->create(x, y);
    } else {
        this->annihilate(x);
    }
}