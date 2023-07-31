#ifndef ABSTRACT_PROCESS_H
#define ABSTRACT_PROCESS_H
    #include "abstractProcess.h"
#endif


#include <vector>

class ContactProcess: public AbstractProcess {
    public:
        ContactProcess(float contaminationRate, int systemSize);

        void create(int x, int y);
        void annihilate(int x);

        void monteCarloStep();

    protected:
        void updateDensity();
        
    private:
        int particleCount;
};