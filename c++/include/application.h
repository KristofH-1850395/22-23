#include "dictItem.h"
#include <vector>
#include <string>

// this helper class hosts the following functions:
// write data will write the data to a csv file
// average data will average the data over all simulations

class Application {
    public:
        //static functions
        static void writeData(std::vector<std::pair<double, double>> data, float infectionRate, int systemSize, std::string path);
        static std::vector<std::pair<double, double>> averageData(std::vector<dictItem> dataDict);
        static void simulateContactProcess(int simTime, int ensembleSize, float infectionRate, int latticeSize, std::string filePath);
        static void simulateBachelorProcess(int simTime, int ensembleSize, float infectionRate, int latticeSize, std::string filePath);
};

