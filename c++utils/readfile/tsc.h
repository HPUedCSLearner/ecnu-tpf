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
protected:
    static uint64_t getOneSecondTsc();
};

}