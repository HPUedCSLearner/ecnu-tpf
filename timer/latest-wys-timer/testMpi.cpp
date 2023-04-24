#include <stdio.h>
#include <stack>
#include <mpi.h>

int do_multi(int a, int b)
{
	return a * b;
}
 
 
int do_calc(int a, int b)
{
	// std::stack<int> st;
	// st.push(23);
	return do_multi(a, b);
}
 
 
int main()
{
	int comm_sz,my_rank;
    MPI_Init(NULL,NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

	int a = 4, b = 5;
	printf("result: %d\n", do_calc(a, b));
	MPI_Finalize();
	return 0;

	
}