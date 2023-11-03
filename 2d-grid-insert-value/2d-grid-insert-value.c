


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef double Data;

typedef struct Matrix
{
    int m, n;
    Data* data;
}Matrix;

void initMatrixWithVal(Matrix* matrix, int m, int n, Data val) {
    matrix->m = m;
    matrix->n = n;
    matrix->data = (Data*)malloc(m * n * sizeof(Data));

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j <  n; ++j) {
            matrix->data[i * matrix->n + j] = val;
        }
    }
} 
void initMatrix(Matrix* matrix, int m, int n) {
    matrix->m = m;
    matrix->n = n;
    matrix->data = (Data*)malloc(m * n * sizeof(Data));

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j <  n; ++j) {
            matrix->data[i * matrix->n + j] = i * j * 10 / 3 + i + 1;
        }
    }
} 

void freeMatrix(Matrix* matrix) {
    if (matrix->data) {
        free(matrix->data);
    }
}

void printMatrix(const Matrix* matrix) {
    if (matrix == NULL || matrix->data == NULL) {
        printf("null ptr occured!!!\n");
        return;
    }
    for (int i = 0; i < matrix->m; ++i) {
        for (int j = 0; j < matrix->n; ++j) {
            printf("%lf\t", matrix->data[i * matrix->n + j]);
        }
        printf("\n");
    }
}

// #define BEBUG

bool insert_2d_value(const Matrix* srcMatrix, Matrix* resMatrix) {
    int m = srcMatrix->m;
    int n = srcMatrix->n;
    if (m < 2 || n < 2) {
        printf("occured: m <= 2 || n <= 2\n");
        return false;
    }
    Data* data = srcMatrix->data;

    // 赋原始值
    resMatrix->m = 2 * m - 1;
    resMatrix->n = 2 * n - 1;
    initMatrixWithVal(resMatrix, resMatrix->m, resMatrix->n, 0);

#ifdef BEBUG
    printMatrix(resMatrix);
    printf("=====================================\n");
#endif

    for(int i = 0; i < m; ++i) {
        int resM = 2 * i;
        for(int j = 0; j < n; ++j) {
            int resN = 2 * j;
            resMatrix->data[resM * resMatrix->n + resN] = data[i * n + j];
            
        }
    }

#ifdef BEBUG
    printMatrix(resMatrix);
    printf("=====================================\n");
#endif

    // 开始插值
    for(int i = 0; i < resMatrix->m; ++i) {
        for (int j = 0; j < resMatrix->n; ++j) {
            int idx = i * resMatrix->n + j;
            // 如果是奇数行
            if (i & 0x1) {      
                if (j & 0x1) {  // 如果是奇数列
                    Data up_left = resMatrix->data[idx - resMatrix->n - 1];
                    Data up_rigt = resMatrix->data[idx - resMatrix->n + 1];
                    Data dn_left = resMatrix->data[idx + resMatrix->n - 1];
                    Data dn_rigt = resMatrix->data[idx + resMatrix->n + 1];
                    resMatrix->data[idx] = (up_left + up_rigt + dn_left + dn_rigt) / 4;
                } else {        // 如果是偶数列
                    Data up = resMatrix->data[idx - resMatrix->n];
                    Data dn = resMatrix->data[idx + resMatrix->n];
                    resMatrix->data[idx] = (up + dn) / 2;
                }
            // 如果是偶数行
            } else {            
                if (j & 0x1) {  // 如果是奇数列
                    Data left = resMatrix->data[idx-1];
                    Data rigt = resMatrix->data[idx+1];
                    resMatrix->data[idx] = (left + rigt) / 2;
                }
            }
        }
    }
    return true;
}

void test() {
    // test API of initMatrix PrintMatrix 
    printf("=====================================\n");
    Matrix srcMatrix;
    // initMatrixWithVal(&srcMatrix, 2, 3, 14);
    initMatrix(&srcMatrix, 3, 4);
    // initMatrix(&srcMatrix, 4, 6);
    printMatrix(&srcMatrix);


    // test API of insert_2d_value
    printf("=====================================\n");
    Matrix resMatrix;

    insert_2d_value(&srcMatrix, &resMatrix);
    printMatrix(&resMatrix);


    // free memmroy
    freeMatrix(&srcMatrix);
    freeMatrix(&resMatrix);
}

int main()
{
    test();
    return 0;
}
