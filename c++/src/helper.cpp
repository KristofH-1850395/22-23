#include "../include/helper.h"
#include <fstream>
#include <iostream>
using namespace std;

void Helper::writeData(vector<pair<double, double>> data, float infectionRate, string path) {
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

vector<pair<double, double>> Helper::averageData(std::vector<dictItem> dataDict) {
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
      std::cout << "averaging data point " << i << " of "
           << dataDict[0].getValues().size() << endl;
    }

    // calculate the average
    average /= dataDict.size();
    
    // add the average to the averageData vector
    averageData[i].first=dataDict[0].getValues()[i].first;
    averageData[i].second=average;
  }
  // return averageData
  return averageData;
}