#pragma once

#include <string>

namespace MyUtils
{

class TSC
{
public:
    static uint64_t getTsc();
    static std::string getConstCpuHz();
    static uint64_t getAvrgOneSecondTsc();
    static uint64_t getOneNanoTsc();
protected:
    static uint64_t getOneSecondTsc();
    // static uint64_t getOneNanoTsc();
};

}