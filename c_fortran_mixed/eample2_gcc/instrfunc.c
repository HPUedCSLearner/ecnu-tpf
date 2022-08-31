
#include "instrfunc.h"

#include <stdio.h>


static int depth = 1;


void __attribute__((no_instrument_function))
printIndent(const int count) {
	for (int i = 0; i < count; ++i) {
		printf("-");
	}
	printf("\n");
}

#define DUMP(func, call) \
	printf("%s: func = %p, called by = %p\n", __FUNCTION__, func, call)
 
 
void __attribute__((no_instrument_function))
__cyg_profile_func_enter(void *this_func, void *call_site)
{
	printIndent(depth++);
	DUMP(this_func, call_site);
}
 
 
void __attribute__((no_instrument_function))
__cyg_profile_func_exit(void *this_func, void *call_site)
{
	printIndent(depth--);
	DUMP(this_func, call_site);
}
 

