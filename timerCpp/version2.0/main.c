
#include <stdio.h>



void BB() {
}

void AA() {
    BB();
}

int main() {
    // AA();
    // AA();
    BB();
    BB();
    BB();
    return 0;
}
