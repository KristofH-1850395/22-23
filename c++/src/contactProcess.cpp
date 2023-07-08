#include "../include/contactProcess.h"

// constructor
ContactProcess::ContactProcess(float infectionRate, int systemSize) {
  this->infectionRate = infectionRate;
  this->density = 1;
  this->creationProbability = infectionRate / (1 + infectionRate);
  this->latticeSize = systemSize;
  this->particleCountA = latticeSize;
  for (int i = 0; i < latticeSize; i++) {
    lattice.push_back(1);
  }
}

void ContactProcess::create(int x, int y) {
  if (this->lattice[x] == 1 && this->lattice[y] == 0) {
    this->lattice[y] = 1;
    this->particleCountA++;
  }
  calculateDensity();
}

void ContactProcess::annihilate(int x) {
  if (this->lattice[x] == 1) {
    this->lattice[x] = 0;
    this->particleCountA--;
  }
  calculateDensity();
}

void ContactProcess::calculateDensity() {
  this->density = (float)this->particleCountA / (float)this->latticeSize;
}