#include "../include/application.h"
#include "../include/bachelorProcess.h"
#include "../include/contactProcess.h"
#include <fstream>
#include <iostream>
#include "omp.h"

void Application::writeData(std::vector<std::pair<double, double>> data, float infectionRate, int latticeSize, std::string filePath) {
    // write avg_data to output.csv
    std::ofstream output(filePath + "lambda_" + std::to_string(infectionRate) + "_size_" + std::to_string(latticeSize) + ".csv");
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

void Application::simulateContactProcess(int simulationTime, int ensembleSize, float infectionRate, int latticeSize, std::string filePath) {
    std::vector<dictItem> dataDict;

    for (int i = 0; i < ensembleSize; i++) {
        // report progress every 100 simulations
        if (i % 100 == 0) {
            std::cout << "for infectionRate: " << infectionRate <<  " --- running simulation " << i << " of " << ensembleSize << std::endl;
        }

        ContactProcess process(infectionRate, latticeSize);

        // define the duration of a MC step and set meassuring parameters
        double mcDuration = 1 / (latticeSize * process.getNormalisationFactor());
        double time = 0;
        double measuringInterval = simulationTime / 4000.0; // we don't want too many data points
        double timeSinceMeasurement = 0;

        // add the initial density to the dataDict    
        dataDict.push_back(dictItem(std::vector<std::pair<float, float>>()));
        dataDict[i].addValue(std::make_pair(time, process.getDensity()));

        // run the simulation
        while (time < simulationTime) {
            if (process.getDensity() != 0) {
                process.monteCarloStep();
            }
            time += mcDuration;
            timeSinceMeasurement += mcDuration;

            if (timeSinceMeasurement >= measuringInterval) {
                dataDict[i].addValue(std::make_pair(time, process.getDensity()));
                timeSinceMeasurement = 0;
            }
        }
    }

    // write metadata to meta.txt
    std::ofstream metadata(filePath + "metadata.txt");
    std::string metadataString = "simulation time: " + std::to_string(simulationTime) + "\n";
    metadataString += "ensemble size: " + std::to_string(ensembleSize) + "\n";    
    metadata << metadataString;

    // average the data and write to file  
    std::cout << "averaging data" << std::endl; 
    std::vector<std::pair<double, double>> avg_data = Application::averageData(dataDict);
    std::cout << "writing data" << std::endl; 
    Application::writeData(avg_data, infectionRate, latticeSize, filePath);
}

void Application::simulateBachelorProcess(int simulationTime, int ensembleSize, float infectionRate, int latticeSize, std::string filePath) {
    std::vector<dictItem> dataDict;

    for (int i = 0; i < ensembleSize; i++) {
        // report progress every 100 simulations
        if (i % 100 == 0) {
            std::cout << "for infectionRate: " << infectionRate <<  " --- running simulation " << i << " of " << ensembleSize << std::endl;
        }

        BachelorProcess lattice(infectionRate, latticeSize);

        // define the duration of a MC step and set meassuring parameters
        double mcDuration = 1 / (latticeSize * lattice.getNormalisationFactor());
        double time = 0;
        double measuringInterval = simulationTime / 4000.0; // we don't want too many data points
        double timeSinceMeasurement = 0;

        // add the initial density to the dataDict    
        dataDict.push_back(dictItem(std::vector<std::pair<float, float>>()));
        dataDict[i].addValue(std::make_pair(time, lattice.getDensity()));

        // run the simulation
        while (time < simulationTime) {
            if (lattice.getDensity() != 0) {
                lattice.monteCarloStep();
            }
            time += mcDuration;
            timeSinceMeasurement += mcDuration;

            if (timeSinceMeasurement >= measuringInterval) {
                dataDict[i].addValue(std::make_pair(time, lattice.getDensity()));
                timeSinceMeasurement = 0;
            }
        }
    }

    // write metadata to meta.txt
    std::ofstream metadata(filePath + "metadata.txt");
    std::string metadataString = "simulation time: " + std::to_string(simulationTime) + "\n";
    metadataString += "ensemble size: " + std::to_string(ensembleSize) + "\n";    
    metadata << metadataString;

    // average the data and write to file
    std::cout << "averaging data" << std::endl;
    std::vector<std::pair<double, double>> avg_data = Application::averageData(dataDict);
    std::cout << "writing data" << std::endl;
    Application::writeData(avg_data, infectionRate, latticeSize, filePath);
}