#include "../../include/application.h"

#include <string>
#include <iostream>
#include <fstream>

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

    // run the simulation for contaminationRate +- a delta
    int range = 4;
    int iteration = 1;

    float diff = ((contaminationRate + 0.01) - (contaminationRate - 0.01)) / 2;
    float delta = diff / range;

    // for (double lambda = contaminationRate - (delta * range); lambda <= contaminationRate + (delta * range); lambda += delta) {
    //     std::cout << "Iteration " << iteration << "/" << range * 2 << std::endl;
    //     Application::simulatePiProcess(simulationTime, ensembleSize, lambda, 1000, outputPath);

    //     iteration++;
    // }

    Application::simulatePiProcess(simulationTime, ensembleSize, contaminationRate, 1000, outputPath);

    return 0;
}
