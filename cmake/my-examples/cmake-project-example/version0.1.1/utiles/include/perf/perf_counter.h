#pragma once
#include <stdint.h> 
#include <string>


namespace myPerf {

class Perf {
public:
static uint64_t getTsc();
static std::string getConstCpuHz();

};

}