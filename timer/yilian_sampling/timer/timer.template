#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>
#include <time.h>
#include "comm.h"
#include "stack.h"
#include "rbtree.h"

int __profile__funcID;

int __profile__fatherID=FUNCTION_ID_NONE;

struct stack __profile__S;//record funcID

struct stack __profile__module_stack;

struct stack __profile__shell_time;

extern int __profile__rank;

int __profile__module_func_ID[MAX_MODULE];

int __profile__num_of_line=0;

struct node *T[9000];

extern void init_stack(struct stack* s);
extern void push(struct stack* s, unsigned long long data);
extern unsigned long long pop(struct stack* s);



void itoa (int n,char s[])
{
	int i,j,sign,len;
	len=0;
	if((sign=n)<0)//记录符号
	n=-n;//使n成为正数
	i=0;
	do{
		s[i++]=n%10+'0';//取下一个数字
		len++;
	}
	while ((n/=10)>0);//删除该数字
	if(sign<0)
		s[i++]='-';
	for(j=0;j<len/2;j++)
	{
		int temp;
		temp=s[j];
		s[j]=s[len-j-1];
		s[len-j-1]=temp;
	}
	s[i]='\0';
}


void __profile__initialize_table()
{
	init_stack(&__profile__S);
	init_stack(&__profile__shell_time);
	init_stack(&__profile__module_stack);
	FILE *fp; 
	
	fp = fopen("${CASEPATH}/sampling/new_usrDF.csv","r");
	char buf[1024];
	while(fgets(buf,1024,fp) != NULL)
		__profile__num_of_line++;
	
	for(int i=0;i<__profile__num_of_line+1;i++)
	{
		T[i]=NULL;
	}
	
	for(int i=0;i<16;i++)//initialize __profile__module_func_ID
		__profile__module_func_ID[i]=-10;
	

	push(&__profile__module_stack,15);
}
void push_moduleid_(int *module_id)
{
	push(&__profile__module_stack,*module_id);
}

void pop_moduleid_()
{
	pop(&__profile__module_stack);
}
unsigned long long eax, edx,shelltimebegin,shelltime;
unsigned long long __profile__record_time_begin()
{
	
	asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));

	push(&__profile__shell_time,(unsigned long long)eax | (unsigned long long)edx << 32);
	
	push(&__profile__S,__profile__funcID);
	
    asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));

	return (unsigned long long)eax | (unsigned long long)edx << 32;
}

unsigned long long module_num;
unsigned long long func_begin_time;

void __profile__record_time_end(char *name,unsigned long long b)
{
	
	__profile__funcID=__profile__S.sta[__profile__S.top];
	__profile__fatherID=__profile__S.sta[__profile__S.top-1];
	
	int search_result=search(T[__profile__funcID],__profile__fatherID,0,b);
	if(search_result==0)
	{
		struct fatherNode __profile__node;
		__profile__node.fatherID=__profile__fatherID;
		for(int i=0;i<16;i++)
		{
			__profile__node.times[i]=0;
			__profile__node.accTime[i]=0;
			__profile__node.shelltime[i]=0;
		}

		unsigned long long module_num=__profile__module_stack.sta[__profile__module_stack.top];
		__profile__node.times[module_num]=1;
		asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));
		__profile__node.accTime[module_num]=((unsigned long long)eax | (unsigned long long)edx << 32) - b;
		
		pop(&__profile__S);
			
		unsigned long long func_begin_time=pop(&__profile__shell_time);
		asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));
		__profile__node.shelltime[module_num]=(((unsigned long long)eax | (unsigned long long)edx << 32) - func_begin_time);
		
		insert(&T[__profile__funcID],__profile__node);
	}
}

void __profile__input_csv()
{
	// char buf[1024];  
	FILE *fr,*fw;     
	
	char filename[1024] = "${CASEPATH}/sampling/result_module/";
	char number[10];
	itoa(__profile__rank,number);
	strcat(filename,number);
	strcat(filename,".csv");
		
	fw = fopen(filename,"w");
	int i,j;
	for(i=0;i<__profile__num_of_line+1;i++)
	{
		inorder(T[i],i,fw);
	}
}

