#include "gemm_api.h"
#include <stdio.h>

void my_dgemm(
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

    // printf("m=%d, n=%d, k=%d, lda=%d, ldb=%d, ldc=%d\n", m, n, k, lda, ldb, ldc);
    
    // ************************************OPT_0****************************************
    // 计算 m * n * k * 2 flops
    // 访存 Read A (m * n * k); Read B (m * n * k); Read & Write C(m * n * k * 2) ; 
    // Total m * n * k * 4
    // for ( i = 0; i < m; i ++ ) {
    //     for ( j = 0; j < n; j ++ ) {
    //         for ( p = 0; p < k; p ++ ) {
    //             C[ i * ldc + j ] += A[ i * lda + p ] * B[ p * ldb + j ];
    //         }
    //     }


    // ************************************OPT_1****************************************
    // 计算 m * n * k * 2 flops
    // 访存 Read A (m * n * k); Read B (m * n * k); Write C(m * n ) ; 
    // Total m * n * k * 2 + m * n
    // double tmp;
    // for ( i = 0; i < m; i ++ ) {
    //     for ( j = 0; j < n; j ++ ) {
    //         tmp = 0;
    //         for ( p = 0; p < k; p ++ ) {
    //             tmp += A[ i * lda + p ] * B[ p * ldb + j ];
    //         }
    //         C[ i * ldc + j ] += tmp;
    //     }
    // }

    // 在上面的基础上，使用寄存器（效果暂时不理想）
    // register double tmp = 0;
    // for ( i = 0; i < m; i ++ ) {
    //     for ( j = 0; j < n; j ++ ) {
    //         tmp = 0;
    //         for ( p = 0; p < k; p ++ ) {
    //             tmp += A[ i * lda + p ] * B[ p * ldb + j ];
    //         }
    //         C[ i * ldc + j ] += tmp;
    //     }
    // }


    // ************************************OPT_2****************************************
    // 优化方法: [[一次计算C的1*4个元素]]
    // 计算 m * n * k * 2 flops
    // 访存 Read A (m * n * k); Read B (m * n * k); Write C(m * n ) ; 
    // Total m * n * k * 2 + m * n
    // double tmp1, tmp2, tmp3, tmp4;
    // for ( i = 0; i < m; i++ ) {
    //     for ( j = 0; j < n; j += 4 ) {
    //         tmp1 = 0;
    //         tmp2 = 0;
    //         tmp3 = 0;
    //         tmp4 = 0;
    //         for ( p = 0; p < k; p++ ) {
    //             tmp1 += A[ i * lda + p ] * B[ p * ldb + j + 0];
    //             tmp2 += A[ i * lda + p ] * B[ p * ldb + j + 1];
    //             tmp3 += A[ i * lda + p ] * B[ p * ldb + j + 2];
    //             tmp4 += A[ i * lda + p ] * B[ p * ldb + j + 3];
    //         }
    //         C[ i * ldc + j + 0] += tmp1;
    //         C[ i * ldc + j + 1] += tmp2;
    //         C[ i * ldc + j + 2] += tmp3;
    //         C[ i * ldc + j + 3] += tmp4;
    //     }
    // }

    // 在上面的基础上，使用tmpA 暂存 A[ i * lda + p ]
    // 分析: 效果较大的原因，可能是因为cache不够，导致A[ i * lda + p ]被换出，需要重新访存
    // 分析: 矩阵越大，效果越明显，说明A[ i * lda + p ]被换出，确实设这样的
    // double tmp1, tmp2, tmp3, tmp4;
    // double tmpA;
    // for ( i = 0; i < m; i++ ) {
    //     for ( j = 0; j < n; j += 4 ) {
    //         tmp1 = 0;
    //         tmp2 = 0;
    //         tmp3 = 0;
    //         tmp4 = 0;
    //         for ( p = 0; p < k; p++ ) {
    //             tmpA  = A[ i * lda + p ];
    //             tmp1 += tmpA * B[ p * ldb + j + 0];
    //             tmp2 += tmpA * B[ p * ldb + j + 1];
    //             tmp3 += tmpA * B[ p * ldb + j + 2];
    //             tmp4 += tmpA * B[ p * ldb + j + 3];
    //         }
    //         C[ i * ldc + j + 0] += tmp1;
    //         C[ i * ldc + j + 1] += tmp2;
    //         C[ i * ldc + j + 2] += tmp3;
    //         C[ i * ldc + j + 3] += tmp4;
    //     }
    // }


    // ************************************OPT_3****************************************
    // 优化方法: [[一次计算C的4*4个元素]]
    // 计算 m * n * k * 2 flops
    // 访存 Read A (m * n * k); Read B (m * n * k); Write C(m * n ) ; 
    // Total m * n * k * 2 + m * n
    // double tmp1,  tmp2,  tmp3,  tmp4;
    // double tmp5,  tmp6,  tmp7,  tmp8;
    // double tmp9,  tmp10, tmp11, tmp12;
    // double tmp13, tmp14, tmp15, tmp16;

    // for ( i = 0; i < m; i+= 4 ) {
    //     for ( j = 0; j < n; j += 4 ) {
    //         tmp1 = 0;
    //         tmp2 = 0;
    //         tmp3 = 0;
    //         tmp4 = 0;
            
    //         tmp5 = 0;
    //         tmp6 = 0;
    //         tmp7 = 0;
    //         tmp8 = 0;

    //         tmp9  = 0;
    //         tmp10 = 0;
    //         tmp11 = 0;
    //         tmp12 = 0;

    //         tmp13 = 0;
    //         tmp14 = 0;
    //         tmp15 = 0;
    //         tmp16 = 0;

    //         for ( p = 0; p < k; p++ ) {
    //             tmp1  += A[ (i + 0) * lda + p ] * B[ p * ldb + j + 0];
    //             tmp2  += A[ (i + 0) * lda + p ] * B[ p * ldb + j + 1];
    //             tmp3  += A[ (i + 0) * lda + p ] * B[ p * ldb + j + 2];
    //             tmp4  += A[ (i + 0) * lda + p ] * B[ p * ldb + j + 3];

    //             tmp5  += A[ (i + 1) * lda + p ] * B[ p * ldb + j + 0];
    //             tmp6  += A[ (i + 1) * lda + p ] * B[ p * ldb + j + 1];
    //             tmp7  += A[ (i + 1) * lda + p ] * B[ p * ldb + j + 2];
    //             tmp8  += A[ (i + 1) * lda + p ] * B[ p * ldb + j + 3];

    //             tmp9  += A[ (i + 2) * lda + p ] * B[ p * ldb + j + 0];
    //             tmp10 += A[ (i + 2) * lda + p ] * B[ p * ldb + j + 1];
    //             tmp11 += A[ (i + 2) * lda + p ] * B[ p * ldb + j + 2];
    //             tmp12 += A[ (i + 2) * lda + p ] * B[ p * ldb + j + 3];

    //             tmp13 += A[ (i + 3) * lda + p ] * B[ p * ldb + j + 0];
    //             tmp14 += A[ (i + 3) * lda + p ] * B[ p * ldb + j + 1];
    //             tmp15 += A[ (i + 3) * lda + p ] * B[ p * ldb + j + 2];
    //             tmp16 += A[ (i + 3) * lda + p ] * B[ p * ldb + j + 3];
    //         }

    //         C[ (i + 0) * ldc + j + 0] += tmp1;
    //         C[ (i + 0) * ldc + j + 1] += tmp2;
    //         C[ (i + 0) * ldc + j + 2] += tmp3;
    //         C[ (i + 0) * ldc + j + 3] += tmp4;

    //         C[ (i + 1) * ldc + j + 0] += tmp5;
    //         C[ (i + 1) * ldc + j + 1] += tmp6;
    //         C[ (i + 1) * ldc + j + 2] += tmp7;
    //         C[ (i + 1) * ldc + j + 3] += tmp8;

    //         C[ (i + 2) * ldc + j + 0] += tmp9;
    //         C[ (i + 2) * ldc + j + 1] += tmp10;
    //         C[ (i + 2) * ldc + j + 2] += tmp11;
    //         C[ (i + 2) * ldc + j + 3] += tmp12;

    //         C[ (i + 3) * ldc + j + 0] += tmp13;
    //         C[ (i + 3) * ldc + j + 1] += tmp14;
    //         C[ (i + 3) * ldc + j + 2] += tmp15;
    //         C[ (i + 3) * ldc + j + 3] += tmp16;
    //     }
    // }

    // 在上面的基础上，使用tmpA1, tmpA2, tmpA3, tmpA4 分别去暂存 A[ (i + 0) * lda + p ], A[ (i + 1) * lda + p ], A[ (i + 1) * lda + p ], A[ (i + 1) * lda + p ] 
    // 分析: 效果较大的原因，可能是因为cache不够，导致A[ i * lda + p ]被换出，需要重新访存
    // 分析: 矩阵越大，效果越明显，说明A[ i * lda + p ]被换出，确实设这样的
    double tmp1,  tmp2,  tmp3,  tmp4;
    double tmp5,  tmp6,  tmp7,  tmp8;
    double tmp9,  tmp10, tmp11, tmp12;
    double tmp13, tmp14, tmp15, tmp16;

    double tmpA1, tmpA2, tmpA3, tmpA4;

    for ( i = 0; i < m; i+= 4 ) {
        for ( j = 0; j < n; j += 4 ) {
            tmp1 = 0;
            tmp2 = 0;
            tmp3 = 0;
            tmp4 = 0;
            
            tmp5 = 0;
            tmp6 = 0;
            tmp7 = 0;
            tmp8 = 0;

            tmp9  = 0;
            tmp10 = 0;
            tmp11 = 0;
            tmp12 = 0;

            tmp13 = 0;
            tmp14 = 0;
            tmp15 = 0;
            tmp16 = 0;

            for ( p = 0; p < k; p++ ) {
                tmpA1 = A[ (i + 0) * lda + p ];
                tmpA2 = A[ (i + 1) * lda + p ];
                tmpA3 = A[ (i + 2) * lda + p ];
                tmpA4 = A[ (i + 3) * lda + p ];
                
                tmp1  += tmpA1 * B[ p * ldb + j + 0];
                tmp2  += tmpA1 * B[ p * ldb + j + 1];
                tmp3  += tmpA1 * B[ p * ldb + j + 2];
                tmp4  += tmpA1 * B[ p * ldb + j + 3];

                tmp5  += tmpA2 * B[ p * ldb + j + 0];
                tmp6  += tmpA2 * B[ p * ldb + j + 1];
                tmp7  += tmpA2 * B[ p * ldb + j + 2];
                tmp8  += tmpA2 * B[ p * ldb + j + 3];

                tmp9  += tmpA3 * B[ p * ldb + j + 0];
                tmp10 += tmpA3 * B[ p * ldb + j + 1];
                tmp11 += tmpA3 * B[ p * ldb + j + 2];
                tmp12 += tmpA3 * B[ p * ldb + j + 3];

                tmp13 += tmpA4 * B[ p * ldb + j + 0];
                tmp14 += tmpA4 * B[ p * ldb + j + 1];
                tmp15 += tmpA4 * B[ p * ldb + j + 2];
                tmp16 += tmpA4 * B[ p * ldb + j + 3];
            }

            C[ (i + 0) * ldc + j + 0] += tmp1;
            C[ (i + 0) * ldc + j + 1] += tmp2;
            C[ (i + 0) * ldc + j + 2] += tmp3;
            C[ (i + 0) * ldc + j + 3] += tmp4;

            C[ (i + 1) * ldc + j + 0] += tmp5;
            C[ (i + 1) * ldc + j + 1] += tmp6;
            C[ (i + 1) * ldc + j + 2] += tmp7;
            C[ (i + 1) * ldc + j + 3] += tmp8;

            C[ (i + 2) * ldc + j + 0] += tmp9;
            C[ (i + 2) * ldc + j + 1] += tmp10;
            C[ (i + 2) * ldc + j + 2] += tmp11;
            C[ (i + 2) * ldc + j + 3] += tmp12;

            C[ (i + 3) * ldc + j + 0] += tmp13;
            C[ (i + 3) * ldc + j + 1] += tmp14;
            C[ (i + 3) * ldc + j + 2] += tmp15;
            C[ (i + 3) * ldc + j + 3] += tmp16;
        }
    }

}
