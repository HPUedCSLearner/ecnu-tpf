
Fortran 和 C 符号表分析
Fortran符号表分析
SUBROUTINE adD(a, b, c)
INTEGER, INTENT(in) :: a, b
INTEGER, INTENT(out) :: c
c = a + b
END SUBROUTINE adD
发现，Fortran编译出来的符号表，全是小写，并且会在后面加一个_
gfortran -c add.f990
ar -r libaddf.a add.o
nm -e libaddf.a
add.o:
0000000000000000 T add_

C符号表分析

#include <stdio.h>

extern void add_(void*,void*, void*);

int main() {
    int a = 1, b  = 2, c = 0;
    add_(&a, &b, &c);
    printf("c = %d\n", c);
    return 0;
}
gcc -c main.c
nm -e main.o
                 U add_
0000000000000000 T main
                 U printf
                 U __stack_chk_fail

发现，C编译出来的符号表，原来是什么，就是什么，并且区分大小写

C++符号表分析
 可以预见的是，C++的符号表，在C的基础上，会加一些杂七杂八的东西

使用-Wl,--wrap=symbol包装Fortran库函数可行性
1、符号表可行性（由上面分析可知）
2、fortran的特性：
参数全部为指针
并且没有返回值
可以很好的写wrapper

# add.f90 fortran 库源码
SUBROUTINE adD(a, b, c)
INTEGER, INTENT(in) :: a, b
INTEGER, INTENT(out) :: c
c = a + b
END SUBROUTINE adD



# main.c  C测试代码 
#include <stdio.h>

extern void add_(void*,void*, void*);

int main() {
    int a = 1, b  = 2, c = 0;
    add_(&a, &b, &c);
    printf("c = %d\n", c);
    return 0;
}



# wrapper.c  wraper函数包装器

#include<stdio.h>

void __wrap_add_(void*a, void*b, void*c) {

    printf("call here\n");
    __real_add_(a,b,c);
}


结果显示，调用到wrap里面，并且结果正确
gfortran -c add.f90
ar -r libaddf.a add.o
gcc  main.c wrapper.c -L. -laddf -Wl,wrap=add_
./a.out
call here
c = 3