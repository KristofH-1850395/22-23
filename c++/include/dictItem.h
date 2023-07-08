#include <vector>
using namespace std;

class dictItem {
private:
    std::vector<std::pair<float, float>> values;

public:
    dictItem(std::vector<std::pair<float, float>> values) {this->values = values;}
    std::vector<std::pair<float, float>> getValues() { return this->values; }    
    void addValue(std::pair<float, float> value) {this->values.push_back(value);}
};