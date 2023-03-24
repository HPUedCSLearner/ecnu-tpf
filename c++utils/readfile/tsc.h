#pragma once

#include <string>

namespace MyUtils
{

class TSC
{
public:
    static uint64_t getTsc();
    static std::string getConstCpuHz();
    static uint64_t getAvrgOneSecondTsc();  /* 1GHz means that 1 nano has 1 cpu clock cycle (1 ticks) */
    static uint64_t getOneNanoTsc();
    static uint64_t getTscDiff();
    static double getTicksPerNano();        /* 2.9GHz means that 1 nano has average 2.9 cpu clock cycles (2.9 ticks) */
protected:
    static uint64_t getOneSecondTsc();
    // static uint64_t getOneNanoTsc();
};

}