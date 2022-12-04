/*
基本实现了测量
但是有问题需要解决：
1、内存泄露问题，malloc的内存，在最后没有释放
*/


#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>
#include <time.h>
#include "stack.h"
// #include "rbtree.h"
// #include <athread.h>
#include "perf_counter.h"
#include "get_date.h"
#include <dlfcn.h>
#include "mpi.h"

// #define __DEBUG_ENTER_FUNCNAME__
// #define __DEBUG_EXIT_FUNCNAME__
// #define __DEBUG_STACK_SIZE__
// #define __DEBUG_PRINT__
// #define __DEBUG_TRACEEND__


#define __DEBUG_FUNCNAME__ // dladdr 应该只能在cpp上编译通过

#ifdef __DEBUG_FUNCNAME__
#include <dlfcn.h>
#endif


void __attribute__((no_instrument_function)) __cyg_profile_func_enter(void*, void*);
void __attribute__((no_instrument_function)) __cyg_profile_func_exit(void*, void*);

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


extern void init_stack(struct stack* s);
extern void push(struct stack* s, unsigned long long data);
extern unsigned long long pop(struct stack* s);
extern unsigned long long top(struct stack* s);
extern int  stackSzie(struct stack* s);

struct stack funcTimeStk;
struct stack funcDddrStk;

hash_t *hash = NULL;

int __profile__rank = 0;
int __profile_common_size;

void __profile__input_csv();

void __attribute__((constructor)) traceBegin(void) {
	hash = hash_new();
  init_stack(&funcTimeStk);
  init_stack(&funcDddrStk);
}

void __attribute__((destructor)) traceEnd(void) {
    #ifdef __DEBUG_TRACEEND__
	  fprintf(stdout, "hash size is : %d\n", hash_size(hash));
	  fprintf(stdout, "funcTimeStk size is : %d\n", stackSzie(&funcTimeStk));
	  fprintf(stdout, "funcDddrStk size is : %d\n", stackSzie(&funcDddrStk));
    #endif

  #ifdef __DEBUG_TRACEEND__
  const char **keys = (const char **)malloc(hash_size(hash));
  const char **vals = (const char **)malloc(hash_size(hash));
  int n = 0;
  hash_each(hash, {
    keys[n] = key;
    vals[n] = val;
    n++;
  }); 
  
	fprintf(stdout, "n is %d\n", n);
  for (int i = 0; i < n; ++i) {
    fprintf(stdout, "%s %s\n", (const char *)keys[i], (const char *)vals[i] );
  }
	#endif


  // need to free MEM  ------------------> TO DO

  __profile__input_csv();

// naive print info
  // const char *keys[30];
  // void *vals[30];
  // int n = 0;

  // hash_each(hash, {
  //   keys[n] = key;
  //   vals[n] = val;
  //   n++;
  // });
  // #ifdef __DEBUG_TRACEEND__
	// fprintf(stdout, "n is %d\n", n);
  // for (int i = 0; i < n; ++i) {
  //   fprintf(stdout, "%s - %s\n", (const char *)keys[i], (const char *)vals[i] );
  // }
	// #endif
}

void __profile__input_csv()
{
	if(__profile__rank != 0) return;
	char buf[1024];  
	FILE *fw;     
	char filename[1024] = "./out", number[10];
	strcat(filename,"_time.csv");
	printf("%s\n",filename);
	fw = fopen(filename, "w");
	
  // const char **keys = (const char **)malloc(hash_size(hash));
  // const char **vals = (const char **)malloc(hash_size(hash));
  // int n = 0;
  // hash_each(hash, {
  //   keys[n] = key;
  //   vals[n] = val;
  //   n++;
  // });
  
  const char *keys[3000];
  void *vals[3000];
  int n = 0;

  hash_each(hash, {
    keys[n] = key;
    vals[n] = val;
    n++;
  });

  for (int i = 0; i < n; ++i) {
    fprintf(fw, "%s %s\n", (const char *)keys[i], (const char *)vals[i] );
  }

  // need to free MEM  ------------------> TO DO

  fclose(fw);
}

void __cyg_profile_func_enter(void *func, void *caller) {
  unsigned long long shell_start_time = perf_counter();
  push(&funcTimeStk, shell_start_time);
  push(&funcDddrStk, func);
  unsigned long long acc_start_time = perf_counter();
  push(&funcTimeStk, acc_start_time);
	
}

void __cyg_profile_func_exit(void *func, void *caller) {
  unsigned long long acc_end_time = perf_counter();

  #ifdef __DEBUG_EXIT_FUNCNAME__
	fprintf(stdout, "p: entry %p %p\n", func, caller);
	fprintf(stdout, "p: entry %lx %lx\n", func, caller);
	#endif

	char callee_caller[128] = {0}; // key
  char times_accTime_shlTIme[100 + 100 + 100] = {0}; // value
	// sprintf(callee_caller, "%p<-%lld", func, pop(&funcDddrStk));
	// sprintf(callee_caller, "%p<-%p", func, pop(&funcDddrStk));
  if (stackSzie(&funcDddrStk) == 1) { // 如果是main func
    sprintf(callee_caller, "%p\n%p", pop(&funcDddrStk), caller);
  } else {
    unsigned long long callee = pop(&funcDddrStk);
    unsigned long long caller = top(&funcDddrStk);
    sprintf(callee_caller, "%p\n%p", callee, caller);
  }

  char* new_callee_caller = (char *)malloc(sizeof(callee_caller) + 1);
  memset(new_callee_caller, 0, sizeof(new_callee_caller));
  strcpy(new_callee_caller, callee_caller);


  #ifdef __DEBUG_EXIT_FUNCNAME__
	fprintf(stdout, "callee_caller: %s\n", new_callee_caller);
  #endif

  if (hash_has(hash, new_callee_caller) == 0) {
    #ifdef __DEBUG_EXIT_FUNCNAME__
    fprintf(stdout, "callee_caller: not store key\n");
    #endif
    memset(times_accTime_shlTIme, 0, sizeof(times_accTime_shlTIme));
    sprintf(times_accTime_shlTIme, "\n,%d,%lld,%lld", 1, acc_end_time - pop(&funcTimeStk), perf_counter() - pop(&funcTimeStk));

    char* new_times_accTime_shlTIme = (char *)malloc(sizeof(times_accTime_shlTIme) + 1);
    memset(new_times_accTime_shlTIme, 0, sizeof(times_accTime_shlTIme));
    strcpy(new_times_accTime_shlTIme, times_accTime_shlTIme);

	  hash_set(hash, new_callee_caller, new_times_accTime_shlTIme);

    #ifdef __DEBUG_PRINT__
    fprintf(stdout, "times_accTime_shlTIme  : %s\n", new_times_accTime_shlTIme);
    fprintf(stdout, "hash_get(hash, callee_caller) : %s\n", hash_get(hash, new_callee_caller));
    #endif

  } else {
    #ifdef __DEBUG_PRINT__
    fprintf(stdout, "[else]: callee_caller value : %s\n", hash_get(hash, new_callee_caller));
    #endif
    int time;
    unsigned long long accTime, shlTIme;
    sscanf(hash_get(hash, new_callee_caller), "\n,%d,%lld,%lld", &time, &accTime, &shlTIme);
    #ifdef __DEBUG_PRINT__
    fprintf(stdout, "time:%d, accTime:%lld, shlTIme:%lld\n", time, accTime, shlTIme);
    #endif
    time++;
    accTime += acc_end_time - pop(&funcTimeStk);
    shlTIme += perf_counter() - pop(&funcTimeStk);
    memset(times_accTime_shlTIme, 0, sizeof(times_accTime_shlTIme));
    sprintf(times_accTime_shlTIme, "\n,%d,%lld,%lld", time, accTime, shlTIme);

    char* new_times_accTime_shlTIme = (char *)malloc(sizeof(times_accTime_shlTIme) + 1);
    memset(new_times_accTime_shlTIme, 0, sizeof(times_accTime_shlTIme));
    strcpy(new_times_accTime_shlTIme, times_accTime_shlTIme);

    hash_set(hash, new_callee_caller, new_times_accTime_shlTIme);
    #ifdef __DEBUG_PRINT__
    fprintf(stdout, "callee_caller value : %s\n", hash_get(hash, new_callee_caller));
    #endif
  }
}