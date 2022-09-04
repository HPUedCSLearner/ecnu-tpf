// #pragma once
#ifndef __PERF_COUNTER_H__
#define __PERF_COUNTER_H__

#include <stdint.h>
 
uint64_t perf_counter();

__inline__ uint64_t __attribute__((no_instrument_function)) perf_counter()
{
  uint32_t lo, hi;
  // take time stamp counter, rdtscp does serialize by itself, and is much cheaper than using CPUID
  __asm__ __volatile__ (
      "rdtscp" : "=a"(lo), "=d"(hi)
      );
  return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}
#endif