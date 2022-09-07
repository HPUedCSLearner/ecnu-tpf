
#include <stdio.h>

#include "perf_counter.h"
#include "stack.h"

static FILE *fp_trace;

static struct Stack stk;
static StkPtr stkp = &stk;


__attribute__((no_instrument_function))
void __attribute__((constructor))  traceBegin(void) {
  fp_trace = fopen("func_trace.out", "w");
  stack_init(stkp);
}

__attribute__((no_instrument_function))
void __attribute__((destructor)) traceEnd(void) {
  if (fp_trace != NULL) {
    fclose(fp_trace);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter(void *func, void *caller) {
  ull t1 = perf_counter();
  stack_push(stkp, t1);

  if (fp_trace != NULL) {
    fprintf(fp_trace, "entry %p %p\n", func, caller);
  }

  ull t2 = perf_counter();
  stack_push(stkp, t2);
}

__attribute__((no_instrument_function))
void __cyg_profile_func_exit(void *func, void *caller) {
  ull t3 = perf_counter();
  stack_top(stkp, &stk_data_temp);
  stack_pop(stkp);
  stack_pop(stkp);
  if (fp_trace != NULL) {
    fprintf(fp_trace, "exit %p %p, tsc: %lld\n", func, caller, t3 - stk_data_temp);
  }

  ull t4 = perf_counter();
}