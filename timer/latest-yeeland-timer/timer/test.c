#include <stdio.h>
#include <mpi.h>

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
	MPI_Init(NULL,NULL);
	int a = 4, b = 5;
	printf("result: %d\n", do_calc(a, b));
	return 0;
}