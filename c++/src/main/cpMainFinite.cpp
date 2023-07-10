#include "../../include/application.h"

#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <omp.h>

int main(int argc, char *argv[]) {
    if (argc != 5) {
        std::cout << "Syntax: " << argv[0] << " <simulationTime> <infectionRate> <ensembleSize> <outputPath>" << std::endl;

        return 1;
    }

    std::cout << "executing program" << std::endl;
    
    // int simtime = the first argument
    int simTime = std::atoi(argv[1]);

    // float infectionRate = the second argument
    float infectionRate = std::atof(argv[2]);

    // int ensembleSize = the third argument
    int ensembleSize = std::atoi(argv[3]);

    // string outputPath = the fourth argument
    std::string outputPath = argv[4];

    // run the simulation for infectionRate +- a delta
    double delta = 0.0128;
    int range = 10;

    int iteration = 1;

    // run the simulation for t = 15 to t = 65 in steps of 5
    for (int systemSize = 15; systemSize <= 65; systemSize += 5) {
        std::cout << "Iteration " << iteration << std::endl;
        Application::simulateContactProcess(simTime, ensembleSize, infectionRate, systemSize, outputPath);

        iteration++;
    }

    return 0;
}
