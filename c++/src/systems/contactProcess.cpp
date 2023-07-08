#include "../../include/contactProcess.h"

// constructor
ContactProcess::ContactProcess(float infectionRate, int systemSize) {
  this->infectionRate = infectionRate;
  this->density = 1;
  this->creationProbability = infectionRate / (1 + infectionRate);
  this->latticeSize = systemSize;
  this->particleCount = latticeSize;
  for (int i = 0; i < latticeSize; i++) {
    lattice.push_back(1);
  }
}

void ContactProcess::create(int x, int y) {
  if (this->lattice[x] == 1 && this->lattice[y] == 0) {
    this->lattice[y] = 1;
    this->particleCount++;
  }
  calculateDensity();
}

void ContactProcess::annihilate(int x) {
  if (this->lattice[x] == 1) {
    this->lattice[x] = 0;
    this->particleCount--;
  }
  calculateDensity();
}

void ContactProcess::calculateDensity() {
  this->density = (float)this->particleCount / (float)this->latticeSize;
}

void ContactProcess::mcStepCP(){
  // choose a random index between 0 and latticeSize
  int x = rand() % this->latticeSize;

  // choose a random float between 0 and 1
  float r = (float)rand() / (float)RAND_MAX;

  // attempt to create or annihilate a particle
  if (r <= this->creationProbability) {

    // choose a random d that is either 1 or -1
    int d = rand() % 2;
    if (d == 0) {
      d = -1;
    }

    // calculate the y coordinate
    int y = x + d;

    // periodic boundary conditions
    if (y < 0) {
      y = this->latticeSize - 1;
    } else if (y >= this->latticeSize) {
      y = 0;
    }

    // attempt to create a particle
    this->create(x, y);
  } else {
    this->annihilate(x);
  }
}

void ContactProcess::simContactProcess(int simTime, int ensembleSize, string filePath){
  std::vector<dictItem> dataDict;
  for (int i = 0; i < ensembleSize; i++) {    
    // report progress every 100 simulations
    if (i % 100 == 0) {
      std::cout << "for infectionate: " << this->infectionRate <<  " --- running simulation " << i << " of " << ensembleSize << endl;
    }

    // reset the lattice
    this->particleCount = this->latticeSize;
    for (int j = 0; j < this->latticeSize; j++) {
      this->lattice[j] = 1;
    }
    this->density = 1;

    // define the duration of a MC step and set meassuring parameters
    double mcDuration = 1 / (this->latticeSize * (1 + this->infectionRate));
    double time = 0;
    double meassuringInterval = 0.025; // we don't want too many data points
    double timeSinceMeassurement = 0;

    // add the initial density to the dataDict    
    dataDict.push_back(dictItem(std::vector<std::pair<float, float>>()));
    dataDict[i].addValue(std::make_pair(time, this->density));

    // run the simulation
    while (time < simTime) {
      if (this->density != 0) {
        mcStepCP();
      }
      time += mcDuration;
      timeSinceMeassurement += mcDuration;

      if (timeSinceMeassurement >= meassuringInterval) {
        dataDict[i].addValue(std::make_pair(time, this->density));
        timeSinceMeassurement = 0;
      }
    }
  }

  // average the data and write to file  
  std::cout << "averaging data" << endl; 
  vector<pair<double, double>> avg_data = Helper::averageData(dataDict);
  std::cout << "writing data" << endl; 
  Helper::writeData(avg_data, this->infectionRate, filePath);
}