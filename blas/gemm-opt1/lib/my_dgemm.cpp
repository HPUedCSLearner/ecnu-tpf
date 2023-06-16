#include "gemm_api.h"
#include <stdio.h>
#include <string.h>

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
    // double tmp1,  tmp2,  tmp3,  tmp4;
    // double tmp5,  tmp6,  tmp7,  tmp8;
    // double tmp9,  tmp10, tmp11, tmp12;
    // double tmp13, tmp14, tmp15, tmp16;

    // double tmpA1, tmpA2, tmpA3, tmpA4;

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
    //             tmpA1 = A[ (i + 0) * lda + p ];
    //             tmpA2 = A[ (i + 1) * lda + p ];
    //             tmpA3 = A[ (i + 2) * lda + p ];
    //             tmpA4 = A[ (i + 3) * lda + p ];
                
    //             tmp1  += tmpA1 * B[ p * ldb + j + 0];
    //             tmp2  += tmpA1 * B[ p * ldb + j + 1];
    //             tmp3  += tmpA1 * B[ p * ldb + j + 2];
    //             tmp4  += tmpA1 * B[ p * ldb + j + 3];

    //             tmp5  += tmpA2 * B[ p * ldb + j + 0];
    //             tmp6  += tmpA2 * B[ p * ldb + j + 1];
    //             tmp7  += tmpA2 * B[ p * ldb + j + 2];
    //             tmp8  += tmpA2 * B[ p * ldb + j + 3];

    //             tmp9  += tmpA3 * B[ p * ldb + j + 0];
    //             tmp10 += tmpA3 * B[ p * ldb + j + 1];
    //             tmp11 += tmpA3 * B[ p * ldb + j + 2];
    //             tmp12 += tmpA3 * B[ p * ldb + j + 3];

    //             tmp13 += tmpA4 * B[ p * ldb + j + 0];
    //             tmp14 += tmpA4 * B[ p * ldb + j + 1];
    //             tmp15 += tmpA4 * B[ p * ldb + j + 2];
    //             tmp16 += tmpA4 * B[ p * ldb + j + 3];
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

    // 在上面的基础上，使用临时变量存上B
    // 加速结果: 加速效果稳定到7倍多
    // double tmp1,  tmp2,  tmp3,  tmp4;
    // double tmp5,  tmp6,  tmp7,  tmp8;
    // double tmp9,  tmp10, tmp11, tmp12;
    // double tmp13, tmp14, tmp15, tmp16;

    // double tmpA1, tmpA2, tmpA3, tmpA4;

    // double tmpB1, tmpB2, tmpB3, tmpB4;

    // // 分成4*4的块计算C
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
    //             tmpA1 = A[ (i + 0) * lda + p ];
    //             tmpA2 = A[ (i + 1) * lda + p ];
    //             tmpA3 = A[ (i + 2) * lda + p ];
    //             tmpA4 = A[ (i + 3) * lda + p ];

    //             tmpB1 = B[ p * ldb + j + 0];
    //             tmpB2 = B[ p * ldb + j + 1];
    //             tmpB3 = B[ p * ldb + j + 2];
    //             tmpB4 = B[ p * ldb + j + 3];
                
    //             tmp1  += tmpA1 * tmpB1;
    //             tmp2  += tmpA1 * tmpB2;
    //             tmp3  += tmpA1 * tmpB3;
    //             tmp4  += tmpA1 * tmpB4;

    //             tmp5  += tmpA2 * tmpB1;
    //             tmp6  += tmpA2 * tmpB2;
    //             tmp7  += tmpA2 * tmpB3;
    //             tmp8  += tmpA2 * tmpB4;

    //             tmp9  += tmpA3 * tmpB1;
    //             tmp10 += tmpA3 * tmpB2;
    //             tmp11 += tmpA3 * tmpB3;
    //             tmp12 += tmpA3 * tmpB4;

    //             tmp13 += tmpA4 * tmpB1;
    //             tmp14 += tmpA4 * tmpB2;
    //             tmp15 += tmpA4 * tmpB3;
    //             tmp16 += tmpA4 * tmpB4;
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


    // 在上面的基础上，使用数组，来定义临时变量
    // 预期效果：和上面的效果一致
    // 加速结果: 加速效果稳定到7倍多(总体稍微提升一点)
    double tmpC_rusult[16];
    double tmpA[4];
    double tmpB[4];

    // 分成4*4的块计算C
    for ( i = 0; i < m; i+= 4 ) {
        for ( j = 0; j < n; j += 4 ) {

            memset(tmpC_rusult, 0, sizeof(tmpC_rusult));

            for ( p = 0; p < k; p++ ) {
                // 目前的性能瓶颈是在儿，下面的取数操作，大矩阵都是cache-miss
                tmpA[0] = A[ (i + 0) * lda + p ];  // 这边访存了
                tmpA[1] = A[ (i + 1) * lda + p ];  // 这边也访存了，没有利用上一步访存开销，局部性没有发挥
                tmpA[2] = A[ (i + 2) * lda + p ];  // 这里也是，上一步的局部性浪费了
                tmpA[3] = A[ (i + 3) * lda + p ];

                tmpB[0] = B[ p * ldb + j + 0]; // 取B的数据，是由局部性的
                tmpB[1] = B[ p * ldb + j + 1];
                tmpB[2] = B[ p * ldb + j + 2];
                tmpB[3] = B[ p * ldb + j + 3];
                
                tmpC_rusult[0]  += tmpA[0] * tmpB[0];
                tmpC_rusult[1]  += tmpA[0] * tmpB[1];
                tmpC_rusult[2]  += tmpA[0] * tmpB[2];
                tmpC_rusult[3]  += tmpA[0] * tmpB[3];

                tmpC_rusult[4]  += tmpA[1] * tmpB[0];
                tmpC_rusult[5]  += tmpA[1] * tmpB[1];
                tmpC_rusult[6]  += tmpA[1] * tmpB[2];
                tmpC_rusult[7]  += tmpA[1] * tmpB[3];

                tmpC_rusult[8]  += tmpA[2] * tmpB[0];
                tmpC_rusult[9]  += tmpA[2] * tmpB[1];
                tmpC_rusult[10] += tmpA[2] * tmpB[2];
                tmpC_rusult[11] += tmpA[2] * tmpB[3];

                tmpC_rusult[12] += tmpA[3] * tmpB[0];
                tmpC_rusult[13] += tmpA[3] * tmpB[1];
                tmpC_rusult[14] += tmpA[3] * tmpB[2];
                tmpC_rusult[15] += tmpA[3] * tmpB[3];
            }

            C[ (i + 0) * ldc + j + 0] += tmpC_rusult[0];
            C[ (i + 0) * ldc + j + 1] += tmpC_rusult[1];
            C[ (i + 0) * ldc + j + 2] += tmpC_rusult[2];
            C[ (i + 0) * ldc + j + 3] += tmpC_rusult[3];

            C[ (i + 1) * ldc + j + 0] += tmpC_rusult[4];
            C[ (i + 1) * ldc + j + 1] += tmpC_rusult[5];
            C[ (i + 1) * ldc + j + 2] += tmpC_rusult[6];
            C[ (i + 1) * ldc + j + 3] += tmpC_rusult[7];

            C[ (i + 2) * ldc + j + 0] += tmpC_rusult[8];
            C[ (i + 2) * ldc + j + 1] += tmpC_rusult[9];
            C[ (i + 2) * ldc + j + 2] += tmpC_rusult[10];
            C[ (i + 2) * ldc + j + 3] += tmpC_rusult[11];

            C[ (i + 3) * ldc + j + 0] += tmpC_rusult[12];
            C[ (i + 3) * ldc + j + 1] += tmpC_rusult[13];
            C[ (i + 3) * ldc + j + 2] += tmpC_rusult[14];
            C[ (i + 3) * ldc + j + 3] += tmpC_rusult[15];
        }
    }



// // ************************************OPT_4****************************************
//     // 优化方法: [[一次计算C的4*4个元素]]
//     // 使用行上的buf-pach, 减少访存次数 

//     double tmpC_rusult[16];
//     double tmpA[4];
//     double tmpB[4];

//     const int buf_pack_size = 256;
//     double Abuf[4][buf_pack_size];      // 行优先存储，A是跨行取数的，没有局部性
//     // double Bbuf[4][buf_pack_size];   // 行优先存储，B有局部性
//     int buf_index;

//     // 分成4*4的块计算C
//     for ( i = 0; i < m; i += 4 ) {
//         for ( j = 0; j < n; j += 4 ) {

//             memset(tmpC_rusult, 0, sizeof(tmpC_rusult));

//             for ( p = 0; p < k; p++ ) {

//                 // 给A外挂一个pack; 
//                 buf_index = p % buf_pack_size;
//                 if (buf_index == 0) {
//                     memset(Abuf, 0, sizeof(Abuf));
//                     if (k - 1 - p >= buf_pack_size) {
//                         memcpy(Abuf[0], &A[ (i + 0) * lda + p ], buf_pack_size * sizeof(double));
//                         memcpy(Abuf[1], &A[ (i + 1) * lda + p ], buf_pack_size * sizeof(double));
//                         memcpy(Abuf[2], &A[ (i + 2) * lda + p ], buf_pack_size * sizeof(double));
//                         memcpy(Abuf[3], &A[ (i + 3) * lda + p ], buf_pack_size * sizeof(double));
//                     } else {
//                         memcpy(Abuf[0], &A[ (i + 0) * lda + p ], (k - p)  * sizeof(double));
//                         memcpy(Abuf[1], &A[ (i + 1) * lda + p ], (k - p)  * sizeof(double));
//                         memcpy(Abuf[2], &A[ (i + 2) * lda + p ], (k - p)  * sizeof(double));
//                         memcpy(Abuf[3], &A[ (i + 3) * lda + p ], (k - p)  * sizeof(double));
//                     }
//                 }

//                 tmpA[0] = Abuf[0][buf_index];
//                 // printf("cpy-tmpA[0]: %.30lf\n", tmpA[0]);
//                 tmpA[1] = Abuf[1][buf_index];
//                 tmpA[2] = Abuf[2][buf_index];
//                 tmpA[3] = Abuf[3][buf_index];

//                 // tmpA[0] = A[ (i + 0) * lda + p ];  // 这边访存了
//                 // printf("raw-tmpA[0]: %.30lf\n", tmpA[0]);
//                 // tmpA[1] = A[ (i + 1) * lda + p ];  // 这边也访存了，没有利用上一步访存开销，局部性没有发挥
//                 // tmpA[2] = A[ (i + 2) * lda + p ];  // 这里也是，上一步的局部性浪费了
//                 // tmpA[3] = A[ (i + 3) * lda + p ];

//                 tmpB[0] = B[ p * ldb + j + 0];
//                 tmpB[1] = B[ p * ldb + j + 1];
//                 tmpB[2] = B[ p * ldb + j + 2];
//                 tmpB[3] = B[ p * ldb + j + 3];
                
//                 tmpC_rusult[0]  += tmpA[0] * tmpB[0];
//                 tmpC_rusult[1]  += tmpA[0] * tmpB[1];
//                 tmpC_rusult[2]  += tmpA[0] * tmpB[2];
//                 tmpC_rusult[3]  += tmpA[0] * tmpB[3];

//                 tmpC_rusult[4]  += tmpA[1] * tmpB[0];
//                 tmpC_rusult[5]  += tmpA[1] * tmpB[1];
//                 tmpC_rusult[6]  += tmpA[1] * tmpB[2];
//                 tmpC_rusult[7]  += tmpA[1] * tmpB[3];

//                 tmpC_rusult[8]  += tmpA[2] * tmpB[0];
//                 tmpC_rusult[9]  += tmpA[2] * tmpB[1];
//                 tmpC_rusult[10] += tmpA[2] * tmpB[2];
//                 tmpC_rusult[11] += tmpA[2] * tmpB[3];

//                 tmpC_rusult[12] += tmpA[3] * tmpB[0];
//                 tmpC_rusult[13] += tmpA[3] * tmpB[1];
//                 tmpC_rusult[14] += tmpA[3] * tmpB[2];
//                 tmpC_rusult[15] += tmpA[3] * tmpB[3];
//             }

//             C[ (i + 0) * ldc + j + 0] += tmpC_rusult[0];
//             C[ (i + 0) * ldc + j + 1] += tmpC_rusult[1];
//             C[ (i + 0) * ldc + j + 2] += tmpC_rusult[2];
//             C[ (i + 0) * ldc + j + 3] += tmpC_rusult[3];

//             C[ (i + 1) * ldc + j + 0] += tmpC_rusult[4];
//             C[ (i + 1) * ldc + j + 1] += tmpC_rusult[5];
//             C[ (i + 1) * ldc + j + 2] += tmpC_rusult[6];
//             C[ (i + 1) * ldc + j + 3] += tmpC_rusult[7];

//             C[ (i + 2) * ldc + j + 0] += tmpC_rusult[8];
//             C[ (i + 2) * ldc + j + 1] += tmpC_rusult[9];
//             C[ (i + 2) * ldc + j + 2] += tmpC_rusult[10];
//             C[ (i + 2) * ldc + j + 3] += tmpC_rusult[11];

//             C[ (i + 3) * ldc + j + 0] += tmpC_rusult[12];
//             C[ (i + 3) * ldc + j + 1] += tmpC_rusult[13];
//             C[ (i + 3) * ldc + j + 2] += tmpC_rusult[14];
//             C[ (i + 3) * ldc + j + 3] += tmpC_rusult[15];
//         }
//     }


}
