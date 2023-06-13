#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>


void test_cache_miss_1(int m, int n, int k, int br);

int main(int argc, char **argv)
{
    int    m, n, k, br; 

    if ( argc != 5 ) {
        printf( "Error: require 3 arguments, but only %d provided.\n", argc - 1 );
        exit( 0 );
    }

    sscanf( argv[ 1 ], "%d", &m );
    sscanf( argv[ 2 ], "%d", &n );
    sscanf( argv[ 3 ], "%d", &k );
    sscanf( argv[ 4 ], "%d", &br );

    test_cache_miss_1(m, n, k, br);
    return 0;
}

void test_cache_miss_1(int m, int n, int k, int br)
{
    double *A, *B, *C;
    A = (double*)malloc(sizeof(double) * m * k);
    B = (double*)malloc(sizeof(double) * k * n);
    C = (double*)malloc(sizeof(double) * m * n);

    switch (br)
    {
        case 1:
            for (int i = 0; i < m; ++i) {
                for (int j = 0; j < n; ++j) {
                    for(int p = 0; p < k; ++p) {
                        C[i*j + i] = A[i*k + k] * B[j*k +k];
                    }
                }
            }
            break;
        case 2:
            for (int j = 0; j < n; ++j) {
                for (int i = 0; i < m; ++i) {
                    for(int p = 0; p < k; ++p) {
                        C[i*j + i] = A[i*k + k] * B[j*k +k];
                    }
                }
            }
            break;
        case 3:
            for(int p = 0; p < k; ++p) {
                for (int j = 0; j < n; ++j) {
                    for (int i = 0; i < m; ++i) {
                        C[i*j + i] = A[i*k + k] * B[j*k +k];
                    }
                }
            }
            break;
        default:
            printf("do nothing\n");
            break;
    }

    
    }