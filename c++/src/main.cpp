#include "../include/system.h"
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
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

void writeData(vector<pair<double, double>> data, float infectionRate) {
  // write avg_data to output.csv
  ofstream output("lambda_" + to_string(infectionRate) + ".csv");

  cout << "constructing string" << endl;
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
  vector<pair<double, double>> averageData;
  // loop over each data point
  for (int i = 0; i < dataDict[0].getValues().size(); i++) {
    double average = 0;
    // loop over each simulation
    for (int j = 0; j < dataDict.size(); j++) {
      average += dataDict[j].getValues()[i].second;
    }
    average /= dataDict.size();
    averageData.push_back(
        std::make_pair(dataDict[0].getValues()[i].first, average));
  }
  // return averageData
  return averageData;
}

void mcStep(System &system) {
  // choose a random index between 0 and latticeSize
  int x = rand() % system.getLatticeSize();
  // choose a random float between 0 and 1
  float r = (float)rand() / (float)RAND_MAX;
  if (r <= system.getCreationProbability()) {
    // choose a random d that is either 1 or -1
    int d = rand() % 2;
    if (d == 0) {
      d = -1;
    }
    int y = x + d;
    if (y < 0) {
      y = system.getLatticeSize() - 1;
    } else if (y >= system.getLatticeSize()) {
      y = 0;
    }
    system.create(x, y);
  } else {
    system.annihilate(x);
  }
}

void findCriticalExponent(int simTime, float infectionRate, int ensembleSize) {
  std::vector<dictItem> dataDict;
  for (int i = 0; i < ensembleSize; i++) {
    cout << "running simulation " << i + 1 << " of " << ensembleSize << endl;
    // init the system
    System system(infectionRate);
    // define the duration of a MC step
    double mcDuration = 1 / (system.getLatticeSize() * (1 + infectionRate));
    double time = 0;
    double meassuringInterval = simTime * 0.0001;
    double timeSinceMeassurement = 0;

    dataDict.push_back(dictItem(std::vector<std::pair<float, float>>()));
    dataDict[i].addValue(std::make_pair(time, system.getDensity()));

    while (time < simTime) {
      if (system.getDensity() != 0) {
        mcStep(system);
      }
      time += mcDuration;
      timeSinceMeassurement += mcDuration;

      if (timeSinceMeassurement >= meassuringInterval) {
        dataDict[i].addValue(std::make_pair(time, system.getDensity()));
        timeSinceMeassurement = 0;
      }
    }
  }

  vector<pair<double, double>> avg_data = averageData(dataDict);
  writeData(avg_data, infectionRate);
}

int main(int argc, char *argv[]) {
  // int simtime = the first argument
  int simTime = std::atoi(argv[1]);
  // float infectionRate = the second argument
  float infectionRate = std::atof(argv[2]);
  // int ensembleSize = the third argument
  int ensembleSize = std::atoi(argv[3]);
  findCriticalExponent(simTime, infectionRate, ensembleSize);
  return 0;
}
