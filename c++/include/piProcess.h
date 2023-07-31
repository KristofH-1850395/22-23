#ifndef ABSTRACT_PROCESS_H
#define ABSTRACT_PROCESS_H
    #include "abstractProcess.h"
#endif

#include <vector>

class PiProcess: public AbstractProcess {
    public:
        PiProcess(float contaminationRate, int systemSize);
        
        void create(int x, int y);
        void mix(int x, int y);
        void annihilate(int x);

        void monteCarloStep();

    protected: 
        void updateDensity();

    private:
        float mixingProbability;
        int particleCountA;
        int particleCountB;
};