// main.c
#include <stdio.h>
#include "perf_counter.h"

void CC(){

}

void BB() {
    CC();
}

void AA() {
    BB();
}

int main() {
    perf_counter();
    // AA();
    // BB();
    // CC();
    return 0;
}
