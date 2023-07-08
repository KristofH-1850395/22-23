#include "../../include/contactProcess.h"

#include <string>
#include <iostream>
using namespace std;

int main(int argc, char *argv[]) {
  std::cout << "executing program" << std::endl;
  
  // int simtime = the first argument
  int simTime = std::atoi(argv[1]);

  // float infectionRate = the second argument
  float infectionRate = std::atof(argv[2]);

  // int ensembleSize = the third argument
  int ensembleSize = std::atoi(argv[3]);

  // string outputPath = the fourth argument
  string outputPath = argv[4];

  // run the simulation for infectionRate +- a delta
  double delta = 0.0128;
  int range = 10;
  for (double lambda = infectionRate - (delta * range); lambda <= infectionRate + (delta * range); lambda += delta) {
    ContactProcess system(lambda, 1000);
    system.simContactProcess(simTime, ensembleSize, outputPath);
  }

  return 0;
}
