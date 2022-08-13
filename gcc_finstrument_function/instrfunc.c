#include <stdio.h>
 
int depth = 1;

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
 

int do_multi(int a, int b)
{
	return a * b;
}
 
 
int do_calc(int a, int b)
{
	return do_multi(a, b);
}
 
 
int main()
{
	int a = 4, b = 5;
	printf("result: %d\n", do_calc(a, b));
	return 0;
}