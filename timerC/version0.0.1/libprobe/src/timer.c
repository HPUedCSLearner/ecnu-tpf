// hash size is : 6
// stack size is : 12
// 调用关系栈和时间栈 


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
extern int  stackSzie(struct stack* s);

struct stack funcTimeStk;

hash_t *hash = NULL;

void __attribute__((constructor)) traceBegin(void) {
	hash = hash_new();
  init_stack(&funcTimeStk);
}

void __attribute__((destructor)) traceEnd(void) {
	fprintf(stdout, "hash size is : %d\n", hash_size(hash));
	fprintf(stdout, "stack size is : %d\n", stackSzie(&funcTimeStk));
}

void __cyg_profile_func_enter(void *func, void *caller) {
  unsigned long long shell_start_time = perf_counter();
  push(&funcTimeStk, shell_start_time);
  unsigned long long acc_start_time = perf_counter();
  push(&funcTimeStk, acc_start_time);
	
}

void __cyg_profile_func_exit(void *func, void *caller) {
  #ifdef __DEBUG_ENTER_FUNCNAME__
	fprintf(stdout, "p: entry %p %p\n", func, caller);
	fprintf(stdout, "p: entry %lx %lx\n", func, caller);
	#endif
	char caller_callee[128] = {0};
	sprintf(caller_callee, "%p<-%p", func, caller);
	fprintf(stdout, "caller_callee: %s\n", caller_callee);
	hash_set(hash, caller_callee, "123123");
}