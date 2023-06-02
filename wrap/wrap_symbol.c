#include "wrap_symbol.h"
#include <stdio.h>
#include <stdlib.h>

 
int __real_foo();

int foo()
{
	printf("call foo function\n");
	return 0;
}
 
int __wrap_foo()
{
	printf("call __wrap_foo function\n");
    __real_foo();
	return 0;
};
 


 
