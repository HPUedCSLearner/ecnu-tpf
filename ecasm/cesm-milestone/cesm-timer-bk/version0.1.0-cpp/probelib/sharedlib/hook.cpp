#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#include <iostream>

extern "C"
void __traceBegin_hook() {
	std::cout << "__traceBegin_hook()" << std::endl;
}

extern "C"
void __traceEnd_hook() {
    std::cout << "__traceEnd_hook()" << std::endl;
}

extern "C" // if no extern "C", c++会minglo函数名（c++支持重载的底层原理）
void __entr_cpp_hook(void *func, void *caller) {
    
}

extern "C"
void __exit_cpp_hook(void *func, void *caller) {
    
}