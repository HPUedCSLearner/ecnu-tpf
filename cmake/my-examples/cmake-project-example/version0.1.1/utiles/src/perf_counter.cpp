#include<perf/perf_counter.h>
#include <thread>
#include <sstream>
#include <functional>

namespace myPerf {

uint64_t Perf::getTsc() {
    uint32_t lo, hi;
    // take time stamp counter, rdtscp does serialize by itself, and is much cheaper than using CPUID
    __asm__ __volatile__ (
        "rdtscp" : "=a"(lo), "=d"(hi)
        );
    return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}

std::string Perf::getConstCpuHz() {
    auto tick1 = Perf::getTsc();
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    auto tick2 = Perf::getTsc();
    std::stringstream ss;
    ss << "this cpu constant frequence is :" << static_cast<double>(tick2 -tick1) / 1e9 << "GHz" << std::endl;
    return ss.str();
}

}