#include <vector>
#include <string>
#include <cmath>
#include <vector>
#include <iostream>

#include <omp.h>
#include <stdlib.h>
#include "helper.h"

using namespace std;

class ContactProcess {
public:
  ContactProcess(float infectionRate, int systemSize);
  void create(int x, int y);
  void annihilate(int x);

  void setInfectionRate(float infectionRate) {this->infectionRate = infectionRate;}
  float getInfectionRate() { return this->infectionRate; }

  void setDensity(float density) { this->density = density; }
  float getDensity() { return this->density; }

  void setCreationProbability(float creationProbability) {this->creationProbability = creationProbability;}
  float getCreationProbability() { return this->creationProbability; }

  void setLatticeSize(int latticeSize) {this->latticeSize = latticeSize;}
  int getLatticeSize() { return this->latticeSize; }

  void setLattice(std::vector<int> lattice) { this->lattice = lattice; }
  std::vector<int> getLattice() { return this->lattice; }

  void simContactProcess(int simTime, int ensembleSize, string filePath);
  void mcStepCP();

private:
  void calculateDensity();
  int latticeSize;
  float infectionRate;
  float density;
  float creationProbability;
  std::vector<int> lattice;
  int particleCount;
};