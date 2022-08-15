
#include <cstdint>
#include <iostream>
 
__inline__ uint64_t perf_counter(void)
{
  uint32_t lo, hi;
  // take time stamp counter, rdtscp does serialize by itself, and is much cheaper than using CPUID
  __asm__ __volatile__ (
      "rdtscp" : "=a"(lo), "=d"(hi)
      );
  return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}
 
int main()
{
  uint64_t t1 = perf_counter();
  uint64_t t2 = perf_counter();
  std::cout << t1 << '\n' << t2 << std::endl;
 
  return 0;
}