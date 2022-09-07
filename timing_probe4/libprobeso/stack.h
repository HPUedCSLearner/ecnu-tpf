#ifndef __STACK_H__
#define __STACK_H__

#include "stack.h"
#include <stdbool.h>
#include <string.h>
#include <stdio.h>

#define Max_Recurve_Depth 100000

typedef unsigned long long ull;
typedef struct Stack* StkPtr;
ull stk_data_temp;

void stack_init(StkPtr s);
bool stack_isEmpty(StkPtr s);
bool stack_isFull(StkPtr s);
bool stack_push(StkPtr s, unsigned long long data);
void stack_pop(StkPtr s);
bool stack_top(StkPtr s, unsigned long long *top);
int  stack_size(StkPtr s);

struct Stack
{
    unsigned long long stk[Max_Recurve_Depth];
	int top;
};

inline void stack_init(StkPtr s) {
    memset(s->stk, 0, sizeof(s->stk));
    s->top = -1;
}
inline bool stack_isEmpty(StkPtr s) {
    return s->top == -1;
}
inline bool stack_isFull(StkPtr s) {
    return s->top == Max_Recurve_Depth - 1;
}
inline bool stack_push(StkPtr s, unsigned long long data) {
    if (stack_isFull(s)) {
        printf("push error, stack is full\n");
        return false;
    } else {
        s->stk[++(s->top)] = data;
        return true;
    }
}
inline void stack_pop(StkPtr s) {
    if (!stack_isEmpty(s)) {
        --(s->top);
    }
}
inline bool stack_top(StkPtr s, unsigned long long *top) {
    if (!stack_isEmpty(s)) {
        *top = s->stk[s->top];
        return true;
    } else {
        printf("stack is empty, Error to get top\n");
        return false;
    }
}

inline int stack_size(StkPtr s) {
    return s->top + 1;
}

#endif