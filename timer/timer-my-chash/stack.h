#ifndef __stack_h__
#define __stack_h__


#include "common.h"
#include <stdio.h>

#define DEFAULT_STACK_SIZE (10)


typedef struct Stack {
    ULL stk[DEFAULT_STACK_SIZE];
    int top;
}Stack, *Stack_Ptr;

void stack_init(Stack_Ptr stack_ptr);
void stack_push(Stack_Ptr stack_ptr, ULL data);
void stack_pop(Stack_Ptr stack_ptr);
ULL  get_stack_top_data(Stack_Ptr stack_ptr);
int  get_stack_top_ptr(Stack_Ptr stack_ptr);
bool is_stack_empty(Stack_Ptr stack_ptr);
bool is_stack_full(Stack_Ptr stack_ptr);

void stack_init(Stack_Ptr stack_ptr)
{
    stack_ptr->top = -1;
}
void stack_push(Stack_Ptr stack_ptr, ULL data)
{
    if (is_stack_full(stack_ptr) == true) {
        printf("[error]: stack is full, can not execute push operate!!!\n");
        return;
    }
    stack_ptr->top++;
    stack_ptr->stk[stack_ptr->top] = data;
}
void stack_pop(Stack_Ptr stack_ptr)
{
    if (is_stack_empty(stack_ptr) == true) {
        printf("[error]: stack is empty, can not execute pop operate!!!\n");
        return;
    }
    stack_ptr->top--;
}
ULL get_stack_top_data(Stack_Ptr stack_ptr)
{
    if (is_stack_empty(stack_ptr) == true) {
        printf("[error]: stack is empty, can not execute top operate!!!\n");
        return 666;
    }
    return stack_ptr->stk[stack_ptr->top];
}
int  get_stack_top_ptr(Stack_Ptr stack_ptr)
{
    return stack_ptr->top;
}
bool is_stack_empty(Stack_Ptr stack_ptr)
{
    return stack_ptr->top == -1;
}
bool is_stack_full(Stack_Ptr stack_ptr)
{
    return stack_ptr->top == (DEFAULT_STACK_SIZE - 1); 
}

#endif