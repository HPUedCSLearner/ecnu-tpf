// main.c
#include <stdio.h>
#include "perf_counter.h"



void BB() {
}

void AA() {
    BB();
}

int main() {
    perf_counter();
    AA();
    BB();
    return 0;
}
