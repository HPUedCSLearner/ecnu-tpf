#include "stack.h"
#include "perf_counter.h"
#include <stdio.h>


ull temp;

void test1();
void test2();
void test3();

int main() {

    test2();
    test3();
    return 0;
}

void test2() {
    ull t1 = perf_counter();
    ull t2 = perf_counter();
    printf("tsc t1: %lld, tsc t2: %lld, all tsc: %lld\n", t1, t2, t2 - t1);
}

void test3() {
    ull t1 = perf_counter();
    test1();
    ull t2 = perf_counter();
    printf("tsc t1: %lld, tsc t2: %lld, all tsc: %lld\n", t1, t2, t2 - t1);
}

void test1() {
    struct Stack stk;
    StkPtr stkp = &stk;
    // StkPtr p;
    stack_init(&stk);
    if (stack_isEmpty(&stk))
        printf("stack is empty\n");
    printf("top : %d\n", stk.top);
    stack_push(&stk, 33);
    printf("top : %d\n", stk.top);
    stack_push(&stk, 33);
    printf("top : %d\n", stk.top);
    stack_push(&stk, 33);
    printf("top : %d\n", stk.top);
    stack_push(&stk, 33);
    printf("top : %d\n", stk.top);
    if (stack_isFull(&stk))
        printf("stack is full\n");
    printf("stack size is %d\n", stack_size(&stk));
    stack_pop(&stk);
    printf("stack size is %d\n", stack_size(&stk));


    stack_push(&stk, 2233);
    stack_top(stkp, &temp);
    printf("stack top is %lld\n", temp);

    stack_init(stkp);
    stack_top(stkp, &temp);
    printf("stack top is %lld\n", temp);
}