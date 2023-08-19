#include "../../include/abstractProcess.h"
#include "math.h"

int AbstractProcess::getRandomNeighbour(int x) {
    // choose a random d that is either 1 or -1
    int d = rand() % 2;

    if (d == 0) {
        d = -1;
    }

    // calculate the y coordinate
    int y = x + d;

    // periodic boundary conditions
    if (y < 0) {
        y = this->latticeSize - 1;
    } else if (y >= this->latticeSize) {
        y = 0;
    }

    return y;
}