#include<stdio.h>

void __wrap_add_(void*a, void*b, void*c) {

    printf("call here\n");
    __real_add_(a,b,c);
}