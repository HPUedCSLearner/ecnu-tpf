double clock_timer( void );

void computeError(
        int    ldc,
        int    ldc_ref,
        int    m,
        int    n,
        double *C,
        double *C_ref
        );

void printMatrix(const double* A, int m, int n, int lda);

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
        );

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
        );