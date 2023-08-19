#include "../include/application.h"
#include "../include/piProcess.h"
#include "../include/contactProcess.h"
#include <fstream>
#include <iostream>
#include <cmath>
#include "omp.h"

void Application::writeData(std::vector<std::pair<double, double>> data, float contaminationRate, int latticeSize, std::string filePath) {
    // write avg_data to output.csv
    std::ofstream output(filePath + "lambda_" + std::to_string(contaminationRate) + "_size_" + std::to_string(latticeSize) + ".csv");
    std::string outputString = "t,density\n";

    for (int i = 0; i < data.size(); i++) {
        outputString += std::to_string(data[i].first);
        outputString += ",";
        outputString += std::to_string(data[i].second);
        outputString += "\n";
    }
    output << outputString;
}

std::vector<std::pair<double, double>> Application::averageData(std::vector<dictItem> dataDict) {
    std::vector<std::pair<double, double>> averageData = std::vector<std::pair<double,double>>(dataDict[0].getValues().size(),std::make_pair<double,double>(0,0));
    // loop over each data point
    int nProcessors = omp_get_max_threads();
    omp_set_num_threads(nProcessors);

    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < dataDict[0].getValues().size(); i++) {
        double average = 0;
        // loop over each simulation
        for (int j = 0; j < dataDict.size(); j++) {
            average += dataDict[j].getValues()[i].second;
        }

        // report progress every 1000 data points
        if (i % 1000 == 0) {
            std::cout << "averaging data point " << i << " of " << dataDict[0].getValues().size() << std::endl;
        }

        // calculate the average
        average /= dataDict.size();
        
        // add the average to the averageData vector
        averageData[i].first=dataDict[0].getValues()[i].first;
        averageData[i].second=average;
    }
    return averageData;
}

void Application::simulateContactProcess(int simulationTime, int ensembleSize, float contaminationRate, int latticeSize, std::string filePath) {
    std::vector<dictItem> dataDict;

    for (int i = 0; i < ensembleSize; i++) {
        // report progress every 100 simulations
        if (i % 100 == 0) {
            std::cout << "for contaminationRate: " << contaminationRate <<  " --- running simulation " << i << " of " << ensembleSize << std::endl;
        }

        ContactProcess process(contaminationRate, latticeSize);

        dataDict.push_back(Application::monteCarlo(process, simulationTime));
    }

    // average the data and write to file  
    std::cout << "averaging data" << std::endl; 
    std::vector<std::pair<double, double>> avg_data = Application::averageData(dataDict);
    std::cout << "writing data" << std::endl; 
    Application::writeData(avg_data, contaminationRate, latticeSize, filePath);
}

void Application::simulatePiProcess(int simulationTime, int ensembleSize, float contaminationRate, int latticeSize, std::string filePath) {
    std::vector<dictItem> dataDict;

    for (int i = 0; i < ensembleSize; i++) {
        // report progress every 100 simulations
        if (i % 100 == 0) {
            std::cout << "for contaminationRate: " << contaminationRate <<  " --- running simulation " << i << " of " << ensembleSize << std::endl;
        }

        PiProcess process(contaminationRate, latticeSize);

        dataDict.push_back(Application::monteCarlo(process, simulationTime));
    }    

    // average the data and write to file
    std::cout << "averaging data" << std::endl;
    std::vector<std::pair<double, double>> avg_data = Application::averageData(dataDict);
    std::cout << "writing data" << std::endl;
    Application::writeData(avg_data, contaminationRate, latticeSize, filePath);
}

template <typename Process> dictItem Application::monteCarlo(Process lattice, int simulationTime)
{
    // define the duration of a MC step and set meassuring parameters
    double mcDuration = 1 / (lattice.getLatticeSize() * lattice.getNormalisationFactor());
    double time = 0;
    double measuringInterval = double(simulationTime / (simulationTime * 10));
    double timeSinceMeasurement = 0;

    // add the initial density to the dataDict    
    dictItem data = dictItem(std::vector<std::pair<float, float>>());
    data.addValue(std::make_pair(time, lattice.getDensity()));

    // run the simulation
    while (time < simulationTime) {
        if (lattice.getDensity() != 0) {
            lattice.monteCarloStep();
        }
        time += mcDuration;
        timeSinceMeasurement += mcDuration;

        if (timeSinceMeasurement >= measuringInterval) {
            data.addValue(std::make_pair(time, lattice.getDensity()));
            timeSinceMeasurement = 0;
        }
    }

    return data;
}