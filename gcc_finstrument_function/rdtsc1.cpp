// from https://stackoverflow.com/questions/39151049/on-a-cpu-with-constant-tsc-and-nonstop-tsc-why-does-my-time-drift
#include <time.h>
#include <unistd.h>
#include <iostream>
#include <iomanip>
#include <cstdlib>

static inline unsigned long rdtscp_start(void) {
  unsigned long var;
  unsigned int hi, lo;

  __asm volatile ("cpuid\n\t"
          "rdtsc\n\t" : "=a" (lo), "=d" (hi)
          :: "%rbx", "%rcx");

  var = ((unsigned long)hi << 32) | lo;
  return (var);
}

static inline unsigned long rdtscp_end(void) {
  unsigned long var;
  unsigned int hi, lo;

  __asm volatile ("rdtscp\n\t"
          "mov %%edx, %1\n\t"
          "mov %%eax, %0\n\t"
          "cpuid\n\t"  : "=r" (lo), "=r" (hi)
          :: "%rax", "%rbx", "%rcx", "%rdx");

  var = ((unsigned long)hi << 32) | lo;
  return (var);
  }

/*see https://www.intel.com/content/www/us/en/embedded/training/ia-32-ia-64-benchmark-code-execution-paper.html
 */

using std::cout;
using std::cerr;
using std::endl;

#define CLOCK CLOCK_REALTIME

uint64_t to_ns(const timespec &ts);   // Converts a struct timespec to ns (since epoch).
void view_ticks_per_ns(int runs =10, int sleep =10);

int main(int argc, char **argv) {
    int runs = 10, sleep = 10;
    if (argc != 1 && argc != 3) {
        cerr << "Usage: " << argv[0] << " [ RUNS SLEEP ] \n";
        exit(1);
    } else if (argc == 3) {
        runs = std::atoi(argv[1]);
        sleep = std::atoi(argv[2]);
    }

    view_ticks_per_ns(runs, sleep);
}

void view_ticks_per_ns(int RUNS, int SLEEP) {
// Prints out stream of RUNS tsc ticks per ns, each calculated over a SLEEP secs interval.
    timespec clock_start, clock_end;
    unsigned long tsc1, tsc2, tsc_start, tsc_end;
    unsigned long elapsed_ns, elapsed_ticks;
    double rate; // ticks per ns from each run.

    clock_getres(CLOCK, &clock_start);
    cout <<  "Clock resolution: " << to_ns(clock_start) << "ns\n\n";

    cout << " tsc ticks      " << "ns      " << " tsc ticks per ns\n";
    for (int i = 0; i < RUNS; ++i) {
        tsc1 = rdtscp_start();
        clock_gettime(CLOCK, &clock_start);
        tsc2 = rdtscp_end();
        tsc_start = (tsc1 + tsc2) / 2;

        sleep(SLEEP);

        tsc1 = rdtscp_start();
        clock_gettime(CLOCK, &clock_end);
        tsc2 = rdtscp_end();
        tsc_end = (tsc1 + tsc2) / 2;

        elapsed_ticks = tsc_end - tsc_start;
        elapsed_ns = to_ns(clock_end) - to_ns(clock_start);
        rate = static_cast<double>(elapsed_ticks) / elapsed_ns;

        cout << elapsed_ticks << " " << elapsed_ns << " " << std::setprecision(12) << rate << endl;
    }
}

constexpr uint64_t BILLION {1000000000};

uint64_t to_ns(const timespec &ts) {
  return ts.tv_sec * BILLION + ts.tv_nsec;
}

