#include "../include/system.h"

// constructor
System::System(float infectionRate, int systemSize) {
  this->infectionRate = infectionRate;
  this->density = 1;
  this->creationProbability = infectionRate / (1 + infectionRate);
  this->latticeSize = systemSize;
  this->particleCount = latticeSize;
  for (int i = 0; i < latticeSize; i++) {
    lattice.push_back(1);
  }
}

void System::create(int x, int y) {
  if (this->lattice[x] == 1 && this->lattice[y] == 0) {
    this->lattice[y] = 1;
    this->particleCount++;
  }
  calculateDensity();
}

void System::annihilate(int x) {
  if (this->lattice[x] == 1) {
    this->lattice[x] = 0;
    this->particleCount--;
  }
  calculateDensity();
}

void System::calculateDensity() {
  this->density = (float)this->particleCount / (float)this->latticeSize;
}