#include "../../include/contactProcess.h"
#include "../../include/helper.h"

#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <omp.h>
using namespace std;

void mcStepCP(ContactProcess &system) {
  // choose a random index between 0 and latticeSize
  int x = rand() % system.getLatticeSize();

  // choose a random float between 0 and 1
  float r = (float)rand() / (float)RAND_MAX;

  // attempt to create or annihilate a particle
  if (r <= system.getCreationProbability()) {

    // choose a random d that is either 1 or -1
    int d = rand() % 2;
    if (d == 0) {
      d = -1;
    }

    // calculate the y coordinate
    int y = x + d;

    // periodic boundary conditions
    if (y < 0) {
      y = system.getLatticeSize() - 1;
    } else if (y >= system.getLatticeSize()) {
      y = 0;
    }

    // attempt to create a particle
    system.create(x, y);
  } else {
    system.annihilate(x);
  }
}

void simContactProcess(int systemSize, int simTime, float infectionRate, int ensembleSize, string path) {
  std::vector<dictItem> dataDict;
  for (int i = 0; i < ensembleSize; i++) {
    // report progress every 100 simulations
    if (i % 100 == 0) {
      cout << "for number of sites: " << systemSize <<  " --- running simulation " << i << " of " << ensembleSize << endl;
    }

    // init the system
    ContactProcess system(infectionRate, systemSize);

    // define the duration of a MC step and set meassuring parameters
    double mcDuration = 1 / (system.getLatticeSize() * (1 + infectionRate));
    double time = 0;
    double meassuringInterval = 0.25; // we don't want too many data points
    double timeSinceMeassurement = 0;

    // add the initial density to the dataDict
    dataDict.push_back(dictItem(std::vector<std::pair<float, float>>()));
    dataDict[i].addValue(std::make_pair(time, system.getDensity()));

    // run the simulation
    while (time < simTime) {
      if (system.getDensity() != 0) {
        mcStepCP(system);
      }
      time += mcDuration;
      timeSinceMeassurement += mcDuration;

      if (timeSinceMeassurement >= meassuringInterval) {
        dataDict[i].addValue(std::make_pair(time, system.getDensity()));
        timeSinceMeassurement = 0;
      }
    }
  }

  // average the data and write to file  
  cout << "averaging data" << endl; 
  vector<pair<double, double>> avg_data = Helper::averageData(dataDict);
  cout << "writing data" << endl; 
  Helper::writeData(avg_data, systemSize, path);
}

int main(int argc, char *argv[]) {
  std::cout << "executing program" << std::endl;

  int simTime = 1000;
  float infectionRate = 3.29785;

  // int ensembleSize = the first argument
  int ensembleSize = std::atoi(argv[1]);

  // string outputPath = the second argument
  string outputPath = argv[2];

  // run the simulation for t = 15 to t = 65 in steps of 5
  for (int systemSize = 15; systemSize <= 65; systemSize += 5) {
    simContactProcess(systemSize, simTime, infectionRate, ensembleSize, outputPath);
  }

  return 0;
}
