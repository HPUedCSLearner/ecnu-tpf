// 计算矩阵—矢量乘法 y = a * x
#include <iostream>
#include <complex>
#include <cblas.h>
int main() {
    using namespace std;
    typedef complex<double> Comp; // 定义复数类型
    int Nr = 2, Nc = 3; // 矩阵行数和列数
    // 矩阵和矢量分配内存
    Comp *a = new Comp [Nr*Nc];
    Comp *x = new Comp [Nc];
    Comp *y = new Comp [Nr];
    Comp alpha(1, 0), beta(0, 0);
    // x 矢量赋值
    for (int i = 0; i < Nc; ++i) {
        x[i] = Comp(i+1., i+2.);
    }
    // a 矩阵赋值
    for (int i = 0; i < Nr*Nc; ++i) {
        a[i] = Comp(i+1., i+2.);
    }
    // 做乘法
    cblas_zgemv(CblasColMajor, CblasNoTrans, Nr, Nc, &alpha, a,
        Nr, x, 1, &beta, y, 1);
        
    // 控制行分别输出 x, a, y
    for (int i = 0; i < Nc; ++i) {
        cout << x[i] << "  ";
    }
    cout << "\n" << endl;
    for (int i = 0; i < Nr; ++i) {
        for (int j = 0; j < Nc; ++j) {
            cout << a[i + Nr*j] << "  ";
        }
        cout << endl;
    }
    cout << "\n" << endl;
    for (int i = 0; i < Nr; ++i) {
        cout << y[i] << "  ";
    }

    return 0;
}