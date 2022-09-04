#include <stdio.h>

extern void hash_int(int x);

void test1() {
    hash_int(3);
}

int main() {
    test1();
    return 0;
}