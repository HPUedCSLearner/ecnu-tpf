#include "gemm_api.h"
#include <stdio.h>

void dgemm_ref(
        int    m,
        int    n,
        int    k,
        double *A,
        int    lda,
        double *B,
        int    ldb,
        double *C,
        int    ldc
        )
{
    // Local variables.
    int    i, j, p;

    // Sanity check for early return.
    if ( m == 0 || n == 0 || k == 0 ) return;

    // Reference GEMM implementation.

    printf("m=%d, n=%d, k=%d, lda=%d, ldb=%d, ldc=%d\n", m, n, k, lda, ldb, ldc);
    
    for ( i = 0; i < m; i ++ ) {
        for ( j = 0; j < n; j ++ ) {
            for ( p = 0; p < k; p ++ ) {
                C[ i * ldc + j ] += A[ i * lda + p ] * B[ p * ldb + j ];
            }
        }
    }
}