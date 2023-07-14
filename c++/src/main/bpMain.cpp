#include "../../include/application.h"

#include <string>
#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
    if (argc != 5) {
        std::cout << "Syntax: " << argv[0] << " <simulationTime> <infectionRate> <ensembleSize> <outputPath>" << std::endl;

        return 1;
    }

    std::cout << "executing program" << std::endl;
    
    // int simtime = the first argument
    int simulationTime = std::atoi(argv[1]);

    // float infectionRate = the second argument
    float infectionRate = std::atof(argv[2]);

    // int ensembleSize = the third argument
    int ensembleSize = std::atoi(argv[3]);

    // string outputPath = the fourth argument
    std::string outputPath = argv[4];

    // write metadata to meta.txt
    std::ofstream metadata(outputPath + "metadata.txt");
    std::string metadataString = "simulation time: " + std::to_string(simulationTime) + "\n";
    metadataString += "ensemble size: " + std::to_string(ensembleSize) + "\n";    
    metadata << metadataString;

    // run the simulation for infectionRate +- a delta
    double delta = 0;
    int range = 0;

    int iteration = 1;

    for (double lambda = infectionRate - (delta * range); lambda <= infectionRate + (delta * range); lambda += delta) {
       std::cout << "Iteration " << iteration << "/" << (2 * range) + 1 << std::endl;
        Application::simulateBachelorProcess(simulationTime, ensembleSize, lambda, 1000, outputPath);

        iteration++;
    }

    return 0;
}
