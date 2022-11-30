#include <stdio.h>

void CC()
{
	printf("i am CC()\n");
}

void BB()
{
	CC();
	printf("i am BB()\n");
}
void AA()
{
	printf("i am AA()\n");
	BB();
}

int do_multi(int a, int b)
{
	AA();
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