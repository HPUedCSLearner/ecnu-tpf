#include <iostream>
#include <vector>
#include <math.h>
#include <thread>

#include "lib/gemm_api.h"

void test_dgemm(int m, int n, int k);

int main(int argc, char *argv[]) 
{
    int    m, n, k; 

    if ( argc != 4 ) {
        printf( "Error: require 3 arguments, but only %d provided.\n", argc - 1 );
        exit( 0 );
    }

    sscanf( argv[ 1 ], "%d", &m );
    sscanf( argv[ 2 ], "%d", &n );
    sscanf( argv[ 3 ], "%d", &k );


    test_dgemm( m, n, k );

    return 0;
}

void test_dgemm(int m, int n, int k)
{
    int    i, j, p;
    double *A, *B, *C, *C_ref;
    int    lda, ldb, ldc, ldc_ref;
    double tmp, error, flops;
    double ref_rectime, dgemm_rectime;
    double ref_beg, ref_time, dgemm_beg, dgemm_time;

    A     = (double*)malloc( sizeof(double) * m * k );
    B     = (double*)malloc( sizeof(double) * k * n );
    C     = (double*)malloc( sizeof(double) * m * n );
    C_ref = (double*)malloc( sizeof(double) * m * n );

    lda = k;
    ldb = n;
    ldc = n;
    ldc_ref = n;

    srand48 (time(NULL));

    // Randonly generate points in [ 0, 1 ].
    for ( i = 0; i < m; i++ ) {
        for ( j = 0; j < k; j++ ) {
            A[i*lda +j] = (double)(drand48());	
        }
    }
    for ( i = 0; i < k; i++ ) {
        for ( j = 0; j < n; j++ ) {
            B[i*ldb +j] = (double)(drand48());	
        }
    }

    for ( i = 0; i < m; i ++ ) {
        for ( j = 0; j < n; j ++ ) {
            C[i*ldc + j]      = (double)( 0.0 );	
            C_ref[i*ldc + j]  = (double)( 0.0 );	
        }
    }

    dgemm_beg = clock_timer();
    my_dgemm(m, n, k, A, lda, B, ldb, C, ldc);
    dgemm_time = clock_timer() - dgemm_beg;

    dgemm_beg = clock_timer();
    dgemm_ref(m, n, k, A, lda, B, ldb, C_ref, ldc_ref);
    ref_time = clock_timer() - dgemm_beg;

    // Compute overall floating point operations.
    flops = ( m * n / ( 1000.0 * 1000.0 * 1000.0 ) ) * ( 2 * k );

    printf( "%5d\t %5d\t %5d\t %5.2lf\t %5.2lf\t speedup: %5.2lf\n", 
            m, n, k, flops / dgemm_time, flops / ref_time, ref_time / dgemm_time);

    computeError(ldc, ldc_ref, m, n, C, C_ref );

    free( A     );
    free( B     );
    free( C     );
    free( C_ref );

}






