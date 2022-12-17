#ifndef TIMER_H_
#define TIMER_H_

#include "timer.h"
#include "stack.h"

#define MAX_MODULE 16

extern int __profile__funcID;
extern int __profile__faFuncID;//记录当前函数的父函数编号

extern int __profile__fatherID;

extern struct stack __profile__S;//record funcID

extern struct stack __profile__module_stack;

extern struct stack __profile__shell_time;

extern int __profile__rank;

extern int __profile__module_func_ID[MAX_MODULE];

extern int __profile__num_of_line;

/*int pop_record[20000];
unsigned long long push_time[20000];
unsigned long long pop_time[20000];
int push_pos=0,pop_pos=0;
char module_name[10000][20];*/

struct fatherNode
{
	unsigned int fatherID;
	unsigned long long accTime;  //根据下标确定module
	unsigned long long times;   //根据下标确定module
	unsigned long long shelltime;    //计时函数时间
};

#endif