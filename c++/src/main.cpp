#include "../include/contactProcess.h"
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <omp.h>
using namespace std;

class dictItem {
private:
  std::vector<std::pair<float, float>> values;

public:
  dictItem(std::vector<std::pair<float, float>> values) {
    this->values = values;
  }

  std::vector<std::pair<float, float>> getValues() { return this->values; }
  void addValue(std::pair<float, float> value) {
    ;
    this->values.push_back(value);
    ;
  }
};

void writeData(vector<pair<double, double>> data, float infectionRate, string path) {
  // write avg_data to output.csv
  ofstream output(path + "lambda_" + to_string(infectionRate) + ".csv");
  string outputString = "t,density\n";
  for (int i = 0; i < data.size(); i++) {
    outputString += std::to_string(data[i].first);
    outputString += ",";
    outputString += std::to_string(data[i].second);
    outputString += "\n";
  }
  output << outputString;
}

vector<pair<double, double>> averageData(std::vector<dictItem> dataDict) {
  vector<pair<double, double>> averageData=vector<pair<double,double>>(dataDict[0].getValues().size(),make_pair<double,double>(0,0));
  // loop over each data point
  #pragma omp parallel for schedule(dynamic) num_threads(8)
  for (int i = 0; i < dataDict[0].getValues().size(); i++) {
    double average = 0;
    // loop over each simulation
    for (int j = 0; j < dataDict.size(); j++) {
      average += dataDict[j].getValues()[i].second;
    }

    // report progress every 1000 data points
    if (i % 1000 == 0) {
      cout << "averaging data point " << i << " of "
           << dataDict[0].getValues().size() << endl;
    }

    // calculate the average
    average /= dataDict.size();
    
    // add the average to the averageData vector
    averageData[i].first=dataDict[0].getValues()[i].first;
    averageData[i].second=average;
    /*averageData.push_back(
        std::make_pair(dataDict[0].getValues()[i].first, average));*/
  }
  // return averageData
  return averageData;
}

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

void simContactProcess(int simTime, float infectionRate, int ensembleSize, string path) {
  std::vector<dictItem> dataDict;
  for (int i = 0; i < ensembleSize; i++) {
    // report progress every 100 simulations
    if (i % 100 == 0) {
      cout << "for infectionate: " << infectionRate <<  " --- running simulation " << i << " of " << ensembleSize << endl;
    }

    // init the system
    float expectedCriticalExponent = 3.29785;
    // int systemSize = 2 * (int)pow(simTime, 1/expectedCriticalExponent) + 1;
    int systemSize = 1000;
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
  vector<pair<double, double>> avg_data = averageData(dataDict);
  cout << "writing data" << endl; 
  writeData(avg_data, infectionRate, path);
}

int main(int argc, char *argv[]) {
  std::cout << "executing program" << std::endl;
  
  // int simtime = the first argument
  int simTime = std::atoi(argv[1]);

  // float infectionRate = the second argument
  float infectionRate = std::atof(argv[2]);

  // int ensembleSize = the third argument
  int ensembleSize = std::atoi(argv[3]);

  // string outputPath = the fourth argument
  string outputPath = argv[4];

  // run the simulation for infectionRate +- a delta
  double delta = 0.0128;
  int range = 10;
  for (double i = infectionRate - (delta * range); i <= infectionRate + (delta * range); i += delta) {
     simContactProcess(simTime, i, ensembleSize, outputPath);
  }

  return 0;
}
