#include <stdio.h>

#include "private.h"

#include "utility/stack.h"
#include "utility/perf_counter.h"
#include "utility/get_date.h"
#include "utility/hash.h"
#include "utility/khash.h"

// #define __DEBUG_ENTER_FUNCNAME__
// #define __DEBUG_EXIT_FUNCNAME__
// #define __DEBUG_STACK_SIZE__
// #define __DEBUG_PRINT__
#define __DEBUG_TRACEEND__

struct stack funcTimeStk;
struct stack funcDddrStk;
int maxDepthTimeStk = 0;
int maxDepthDddrStk = 0;

void __self__traceBegin() {
    printf("__self__traceBegin\n");
	init_stack(&funcTimeStk);
	init_stack(&funcDddrStk);
}
void __self__traceEnd() {
    printf("__self__traceEnd\n");
	#ifdef __DEBUG_TRACEEND__
	  // fprintf(stdout, "hash size is : %d\n", hash_size(hash));
	  fprintf(stdout, "funcTimeStk size is : %d\n", stackSzie(&funcTimeStk));
	  fprintf(stdout, "funcDddrStk size is : %d\n", stackSzie(&funcDddrStk));
	  
	  fprintf(stdout, "maxDepthTimeStk is : %d\n", maxDepthTimeStk);
	  fprintf(stdout, "maxDepthDddrStk is : %d\n", maxDepthDddrStk);

    #endif
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
	
	maxDepthTimeStk < stackSzie(&funcDddrStk) ? maxDepthTimeStk = stackSzie(&funcDddrStk) : NULL;
	maxDepthDddrStk < stackSzie(&funcTimeStk) ? maxDepthDddrStk = stackSzie(&funcTimeStk) : NULL;
	
	pop(&funcTimeStk);
	pop(&funcTimeStk);
	pop(&funcDddrStk);
}