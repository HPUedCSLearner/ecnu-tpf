
#include <stdio.h>

static FILE *fp_trace;


__attribute__((no_instrument_function))
void __attribute__((constructor))  traceBegin(void) {
  printf("come cons\n");
  fp_trace = fopen("func_trace.out", "w");
}

__attribute__((no_instrument_function))
void __attribute__((destructor)) traceEnd(void) {
  if (fp_trace != NULL) {
    fclose(fp_trace);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter(void *func, void *caller) {
  if (fp_trace != NULL) {
    fprintf(fp_trace, "entry %p %p\n", func, caller);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_exit(void *func, void *caller) {
  if (fp_trace != NULL) {
    fprintf(fp_trace, "exit %p %p\n", func, caller);
  }
}