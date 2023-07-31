#include "../../include/application.h"

#include <string>
#include <iostream>
#include <fstream>
#include <cmath>

int main(int argc, char *argv[]) {
    if (argc != 5) {
        std::cout << "Syntax: " << argv[0] << " <simulationTime> <contaminationRate> <ensembleSize> <outputPath>" << std::endl;

        return 1;
    }

    std::cout << "executing program" << std::endl;
    
    // int simtime = the first argument
    int simulationTime = std::atoi(argv[1]);

    // float contaminationRate = the second argument
    float contaminationRate = std::atof(argv[2]);

    // int ensembleSize = the third argument
    int ensembleSize = std::atoi(argv[3]);

    // string outputPath = the fourth argument
    std::string outputPath = argv[4];

    // write metadata to meta.txt
    std::ofstream metadata(outputPath + "metadata.txt");
    std::string metadataString = "simulation time: " + std::to_string(simulationTime) + "\n";
    metadataString += "ensemble size: " + std::to_string(ensembleSize) + "\n";    
    metadata << metadataString;
    metadata.close();
    
    int iteration = 1;

    for (int systemSize = 8; systemSize <= pow(2,12); systemSize *= 2) {
        std::cout << "Iteration " << iteration << std::endl;
        Application::simulateContactProcess(simulationTime, ensembleSize, contaminationRate, systemSize, outputPath);

        iteration++;
    }

    return 0;
}
