#include <stdio.h>
#include <stdlib.h>
#include "wrap_symbol.h"

// int __real_foo()
// {
// 	printf("call __real_foo function\n");
// 	return 0;
// };
// int foo()
// {
// 	printf("call foo function\n");
// 	return 0;
// }

int main()
{
	printf("===== test start =====\n");
	char* p1 = (char*)malloc(sizeof(int));
	free(p1);
	foo();
	// int* p2 = new int;
	// delete p2;
 
	printf("===== test finish =====\n");
	return 0;
}
