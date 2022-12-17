#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>
#include <time.h>
// #include "stack.h"
// #include "rbtree.h"
// #include <athread.h>
#include "perf_counter.h"
#include "get_date.h"
#include <dlfcn.h>
#include "mpi.h"

// #define __DEBUG_ENTER_FUNCNAME__
// #define __DEBUG_EXIT_FUNCNAME__
// #define __DEBUG_STACK_SIZE__

#include "hash.h"
/*
 * Set hash `key` to `val`.
 */

inline void
hash_set(hash_t *self, const char *key, void *val) {
  int ret;
  khiter_t k = kh_put(ptr, self, key, &ret);
  kh_value(self, k) = val;
}

/*
 * Get hash `key`, or NULL.
 */

inline void *
hash_get(hash_t *self, const char *key) {
  khiter_t k = kh_get(ptr, self, key);
  return k == kh_end(self) ? NULL : kh_value(self, k);
}

/*
 * Check if hash `key` exists.
 */

inline int
hash_has(hash_t *self, const char *key) {
  if(!hash_size(self)) return 0;
  khiter_t k = kh_get(ptr, self, key);
  return k != kh_end(self);
}

/*
 * Remove hash `key`.
 */

void hash_del(hash_t *self, const char *key) {
  khiter_t k = kh_get(ptr, self, key);
  kh_del(ptr, self, k);
}

hash_t *hash = NULL;

void __attribute__((constructor)) traceBegin(void) {
	hash = hash_new();
}

void __attribute__((destructor)) traceEnd(void) {
	fprintf(stdout, "hash size is : %d\n", hash_size(hash));
}

void __cyg_profile_func_enter(void *func, void *caller) {
	#ifdef __DEBUG_ENTER_FUNCNAME__
	fprintf(stdout, "p: entry %p %p\n", func, caller);
	fprintf(stdout, "p: entry %lx %lx\n", func, caller);
	#endif
	char caller_callee[128] = {0};
	sprintf(caller_callee, "%p<-%p", func, caller);
	fprintf(stdout, "caller_callee: %s\n", caller_callee);
	hash_set(hash, caller_callee, "123123");
	
}

void __cyg_profile_func_exit(void *func, void *fatherFunc) {}











// #define FUNCTION_ID_NONE -1

// int __profile__funcID;//记录当前函数的编号

// int __profile__faFuncID;//记录当前函数的父函数编号

// int __profile__fatherID=FUNCTION_ID_NONE;//记录当前函数的父函数的编号

// struct stack __profile__S;//存有从Main函数到当前函数所有调用函数编号的栈

// struct stack __profile__shell_time;//记录开始计时函数起始时间的栈

// int __profile__rank = 1;//记录当前处在哪个rank中（多进程） ---------------- > TO DO 

// int __profile_common_size;

// int __profile__module_func_ID[MAX_MODULE];

// int __profile__num_of_line=0;//程序拥有的函数数量

// struct node *T[9000];//函数运行信息记录节点

// extern void init_stack(struct stack* s);
// extern void push(struct stack* s, unsigned long long data);
// extern unsigned long long pop(struct stack* s);

// unsigned long addr2int[9001];

// void  __profile__input_csv();

// //int_to_string 转换
// char * myitoa (int n, char *s)
// {
// 	int i,j,sign,len;
// 	len=0;
// 	if((sign=n)<0)//记录符号
// 		n=-n;//使n成为正数
// 	i=0;
// 	do{
// 		s[i++]=n%10+'0';//取下一个数字
// 		len++;
// 	}while((n/=10)>0);//删除该数字
// 	if(sign<0)
// 		s[i++]='-';
// 	for(j=0;j<len/2;j++)
// 	{
// 		char temp;
// 		temp=s[j];
// 		s[j]=s[len-j-1];
// 		s[len-j-1]=temp;
// 	}
// 	s[i]='\0';
// 	return s;
// }

// unsigned long long eax, edx,shelltimebegin,shelltime;
// unsigned long long ic,oc;
// unsigned long long __profile__record_time_begin()
// {
// 	printf("__profile__record_time_begin:%d %d\n",__profile__funcID,__profile__faFuncID);
// 	//记录开始计时函数的开始运行时间
// 	ic=perf_counter();
// 	// printf("stack=%d\n",__profile__shell_time.sta[__profile__shell_time.top]);
// 	//将开始计时函数的开始运行时间压栈
// 	if(__profile__shell_time.sta[__profile__shell_time.top]!=-1&&__profile__shell_time.top==0){
// 		// printf("STACK is NULL!,%d\n",__profile__shell_time.sta[__profile__shell_time.top]);
// 		// if(__profile__rank == 0)printf("ic=%ld\n",ic);
// 		init_stack(&__profile__shell_time);
// 		int i;
// 		for(i=0;i<9000;i++)
// 		{
// 			T[i]=NULL;
// 		}
// 	}
// 	if(__profile__S.sta[__profile__S.top]!=-1&&__profile__S.top==0){
// 		init_stack(&__profile__S);
// 	}
// 	if(__profile__S.top>0)__profile__fatherID=top(&__profile__S);
// 	push(&__profile__S,__profile__funcID);
// 	push(&__profile__shell_time,ic);

// 	//记录开始计时函数的结束运行时间
// 	oc=perf_counter();
// 	push(&__profile__shell_time,oc);
// }

// unsigned long long func_begin_time;

// void __profile__record_time_end()
// {
	
// 	// __profile__funcID=__profile__S.sta[__profile__S.top];//获取当前函数编号
// 	// __profile__fatherID=__profile__S.sta[__profile__S.top-1];//获取当前函数的父函数编号
// 	//判断当前调用关系是否已被记录过，若被记录过，则将函数运行时间进行累加

// 	unsigned long b;
// 	// printf("---->enter record\n");
// 	b=pop(&__profile__shell_time);
	
// 	if(__profile__S.top>0)pop(&__profile__S);
// 	if(__profile__S.top>0)__profile__fatherID=top(&__profile__S);

// 	// printf("##---->b=%ld\n",b);
// 	int search_result=search(T[__profile__funcID],__profile__fatherID,0,b);
// 	if(search_result==0)//若未被记录，则新建一个node，并插入红黑树
// 	{
// 		// printf("search_result=%d %d %d %ld\n",__profile__funcID,__profile__fatherID, search_result,b);
// 		struct fatherNode __profile__node;
// 		__profile__node.fatherID=__profile__fatherID;
// 		__profile__node.times=1;
// 		ic=perf_counter();
// 		__profile__node.accTime=ic - b;

// 		func_begin_time=pop(&__profile__shell_time);
// 		oc=perf_counter();
// 		__profile__node.shelltime=oc-func_begin_time;
// 		insert(&T[__profile__funcID],__profile__node);
// 	}
// 	// pop(&__profile__shell_time);
// 	if(__profile__shell_time.top==1){
// 		MPI_Comm_size(MPI_COMM_WORLD, &__profile_common_size); // ---------------- > TO DO 
// 		MPI_Comm_rank(MPI_COMM_WORLD, &__profile__rank);
// 		// printf("STACK is EMPTY!!%d\n",__profile_common_size);
// 		__profile__input_csv();
// 	}
// }

// // char *filename, *number;
// //将函数运行信息写入硬盘
// void __profile__input_csv()
// {
// 	// if(__profile__rank + 1!= __profile_common_size) return;  ---------------- > TO DO 
// 	char buf[1024];  
// 	FILE *fw;     
// 	// char filename[1024] = "../sampling/timer/out/", number[10];
// 	char filename[1024] = "./", number[10];
// 	myitoa(__profile__rank+1, number);  // ---------------- > TO DO 
// 	strcat(filename,number);
// 	strcat(filename,"__");
// 	strcat(filename, timesStamp());
// 	strcat(filename,".csv");
// 	printf("%s\n",filename);
// 	fw = fopen(filename, "w");
// 	int i,j;
// 	for(i=1;i<9000+1;i++)
// 	{
// 		if(T[i]==NULL)continue;
// 		inorder(T[i],i,fw);
// 	}
//     fclose(fw);
// }

// void __attribute__((no_instrument_function)) debug_log(const char *format,...);
// void __attribute__((no_instrument_function)) __cyg_profile_func_enter(void*, void*);
// void __attribute__((no_instrument_function)) __cyg_profile_func_exit(void*, void*);

// #define MOD (unsigned long)(9000)
// unsigned long addr2int[9001];

// int getHashId(unsigned long oriId){
// 	int tmp=oriId%MOD;
// 	// printf("oriId:%ld\n",oriId);
// 	if(tmp==0)tmp++;
// 	while(addr2int[tmp]!=oriId){
// 		if(addr2int[tmp]==0||addr2int[tmp]==oriId){
// 			addr2int[tmp]=oriId;
// 			return tmp;
// 		}	
// 		tmp++;
// 		if(tmp>9000)tmp=1;
// 	}
// 	return tmp;
// }
// void  __attribute__((no_instrument_function))
// __cyg_profile_func_enter(void *this, void *call)
// {
// 	int funId = getHashId((unsigned long)this), faFuncId = getHashId((unsigned long)call);
// 	// printf("#yes enter:%d %d\n",funId,faFuncId);
// 	__profile__funcID = funId;
// 	__profile__fatherID = faFuncId;
// 	__profile__record_time_begin();
    
// }
 
// void  __attribute__((no_instrument_function))
// __cyg_profile_func_exit(void *this, void *call)
// {
// 	int funId = getHashId((unsigned long)this), faFuncId = getHashId((unsigned long)call);
// 	// printf("#yes exit:%d %d\n",funId,faFuncId);
// 	__profile__funcID = funId;
// 	__profile__fatherID = faFuncId;
// 	__profile__record_time_end();
// }