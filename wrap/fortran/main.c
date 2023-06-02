#include <stdio.h>

extern void add_(void*,void*, void*);

int main() {
    int a = 1, b  = 2, c = 0;
    add_(&a, &b, &c);
    printf("c = %d\n", c);
    return 0;
}