// #pragma once
#ifndef __PERF_COUNTER_H__
#define __PERF_COUNTER_H__

#include <stdint.h>
 
uint64_t perf_counter();

uint32_t lo, hi; // 是否要把这个局部变量优化掉

// __inline__ uint64_t perf_counter()
uint64_t perf_counter()
{
  // uint32_t lo, hi; // 是否要把这个局部变量优化掉
  __asm__ __volatile__ (
      "rdtscp" : "=a"(lo), "=d"(hi)
      );
  return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}
#endif