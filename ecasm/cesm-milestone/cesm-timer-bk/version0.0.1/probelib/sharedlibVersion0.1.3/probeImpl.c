#include <stdio.h>

#include "private.h"

#include "utility/stack.h"
#include "utility/perf_counter.h"
#include "utility/get_date.h"
#include "utility/hash.h"
#include "utility/khash.h"

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


// #define __DEBUG_ENTER_FUNCNAME__
// #define __DEBUG_EXIT_FUNCNAME__
// #define __DEBUG_STACK_SIZE__
// #define __DEBUG_PRINT__
#define __DEBUG_TRACEEND__

struct stack funcTimeStk;
struct stack funcDddrStk;
hash_t *hash = NULL;

void __self__traceBegin() {
    printf("__self__traceBegin\n");
	hash = hash_new();
	init_stack(&funcTimeStk);
	init_stack(&funcDddrStk);
}
void __self__traceEnd() {
    printf("__self__traceEnd\n");

}
void __self__cyg_profile_func_enter(void *func, void *caller) {
    unsigned long long shell_start_time = perf_counter();
    push(&funcTimeStk, shell_start_time);
    push(&funcDddrStk, func);
    unsigned long long acc_start_time = perf_counter();
    push(&funcTimeStk, acc_start_time);
}
void __self__cyg_profile_func_exit(void *func, void *caller) {
    unsigned long long acc_end_time = perf_counter();
	
	char callee_caller[128] = {0}; 								// key
	char times_accTime_shlTIme[100 + 100 + 100] = {0}; 			// value
	if (stackSzie(&funcDddrStk) == 1) { 						// 如果是main func
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