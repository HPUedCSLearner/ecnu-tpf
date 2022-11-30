// main.c
#include <stdio.h>
#include "perf_counter.h"
#include <dlfcn.h>
#include <cxxabi.h>

void CC(){

    Dl_info info1;
}

void BB() {
    CC();
}

void AA() {
    BB();
}

int main() {
    perf_counter();
    AA();
    BB();
    CC();
    return 0;
}
