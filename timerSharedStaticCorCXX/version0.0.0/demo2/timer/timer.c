#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>
#include <time.h>



void __attribute__((constructor)) traceBegin(void) {
}

void __attribute__((destructor)) traceEnd(void) {
}

void __cyg_profile_func_enter(void *func, void *caller) {}

void __cyg_profile_func_exit(void *func, void *fatherFunc) {}
