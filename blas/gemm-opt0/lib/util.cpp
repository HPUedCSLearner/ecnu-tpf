#include <math.h>
#include <stdio.h>
#include<sys/time.h>

#include "gemm_api.h"


// 1微秒 级别 计时器
double clock_timer( void )
{
	struct timeval time_now = {0};
    long time_sec = 0;//秒
    long time_mil = 0;//1毫秒 = 1秒/1000 
    long time_mic = 0;//1微秒 = 1毫秒/1000

    gettimeofday(&time_now, NULL);
    time_sec = time_now.tv_sec;
    time_mil = time_sec * 1000 + time_now.tv_usec/1000;
    time_mic = time_now.tv_sec*1000*1000 + time_now.tv_usec;
    
    return (double)time_mic / 1e6;
}

// 计时器精度校验 代码
    // start = clock_timer();
    // std::this_thread::sleep_for(std::chrono::seconds(1));
    // time = clock_timer() - start;
    // printf("time check : 1 second is %lf\n", time);

    // time check : 1 second is 1.000157

#define TOLERANCE 1E-10
void computeError(
        int    ldc,
        int    ldc_ref,
        int    m,
        int    n,
        double *C,
        double *C_ref
        )

{
    int    i, j;
    for ( i = 0; i < m; i ++ ) {
        for ( j = 0; j < n; j ++ ) {
            if ( fabs( C[i*ldc + j] - C_ref[i*ldc + j] ) > TOLERANCE ) {
                printf( "C[ %d ][ %d ] != C_ref, %E, %E\n", i, j, C[i*ldc + j] , C_ref[i*ldc + j]);
                break;
            }
        }
    }
}


// 默认行优先存储
void printMatrix(const double* A, int m, int n, int lda)
{
    printf("***************************************************\n");
    int i ,j;
    for(i = 0; i < m; ++i) {
        for (j = 0; j < n; ++j) {
            printf("%4.lf", A[i*lda + j]);
        }
        printf("\n");
    }
    printf("+++++++++++++++++++++++++++++++++++++++++++++++++++\n");
}