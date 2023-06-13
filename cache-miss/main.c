#include <stdio.h>
#include <unistd.h>
 
int main(int argc, char **argv)
{
	int a[1000][1000];
	if(1 == argc)
	{
		for(int i = 0; i < 1000; ++i)
		{
				for(int j = 0; j < 1000; ++j)
				{
						a[i][j] = 0;
				}
		}
	}
	else
	{
		for(int i = 0; i < 1000; ++i)
		{
				for(int j = 0; j < 1000; ++j)
				{
						a[j][i] = 0;
				}
		}
	}
 
	return 0;
}
