#include "../include/contactProcess.h"
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <omp.h>
using namespace std;

int main(int argc, char *argv[]) {
    std::cout << "executing program" << std::endl;

    // create BachelorProcess object
    float infectionRate = 0.5;
    int systemSize = 100;
    ContactProcess bachelorProcess = ContactProcess(infectionRate, systemSize);

    // write density to console
    std::cout << "density: " << bachelorProcess.getDensity() << std::endl;

    // destroy half the particles in the system
    for (int i = 0; i < systemSize / 2; i++) {
        bachelorProcess.annihilate(i);
    }

    // write density to console
    std::cout << "density: " << bachelorProcess.getDensity() << std::endl;

    return 0;
}