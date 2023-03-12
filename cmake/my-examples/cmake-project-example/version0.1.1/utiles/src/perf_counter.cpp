#include<perf/perf_counter.h>

namespace myPerf {

uint64_t Perf::getTsc() {
    uint32_t lo, hi;
    // take time stamp counter, rdtscp does serialize by itself, and is much cheaper than using CPUID
    __asm__ __volatile__ (
        "rdtscp" : "=a"(lo), "=d"(hi)
        );
    return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}

}