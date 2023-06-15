#include <vector>
#include <cblas.h>
#include <iostream>

#include <stdio.h>

template<class T>
void printMatrix(const std::vector<T>& data, const int& ld);

int main()
{
    int lda = 8;
    int ldb = 7;
    int ldc = 6;
    int M = 2;
    int N = 3;
    int K = 4;

    float alpha = 1.0;
    float beta  = 0.0;

    std::vector<float> A {
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    };

    std::cout << "A.size()" << " " << A.size() << std::endl;

    std::vector<float> B {
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    };

    std::vector<float> C {
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    };

    M = 2; N = 3; K = lda; // cal C of 2 * 3 block
    cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                M, N, K,
                alpha,
                &A[0], lda, &B[1], ldb,
                beta,
                &C[1], ldc);


    printMatrix<float>(C, ldc);
    return 0;
}

template<class T>
void printMatrix(const std::vector<T>& data, const int& ld)
{
    for(auto i = 0; i < data.size(); ++i) {
        if(i % ld == 0) {
            printf("\n");
        }
        printf("%3.f", data[i]);
    }
    printf("\n");
}