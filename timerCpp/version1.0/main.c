
#include <stdio.h>



void BB() {
}

void AA() {
    BB();
}

int main() {
    AA();
    BB();
    return 0;
}
