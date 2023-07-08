#include "dictItem.h"
#include <vector>
#include <string>
using namespace std;

// this helper class hosts the following functions:
// write data will write the data to a csv file
// average data will average the data over all simulations

class Helper{
    public:
        //static functions
        static void writeData(vector<pair<double, double>> data, float infectionRate, string path);
        static vector<pair<double, double>> averageData(std::vector<dictItem> dataDict);
};

