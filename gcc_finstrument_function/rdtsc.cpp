#include <cstdint>
#include <iostream>
#include <x86intrin.h>

__inline__ uint64_t perf_counter(void)
{
    __asm__ __volatile__("" : : : "memory");
    uint64_t r =  __rdtsc();
    __asm__ __volatile__("" : : : "memory");

    return r;
}

void someFunction() {

}

int main()
{
    uint64_t t1 = perf_counter();
    someFunction();
    uint64_t t2 = perf_counter();
    std::cout << t2 - t1 << " counts" << std::endl;
    
    return 0;
}

