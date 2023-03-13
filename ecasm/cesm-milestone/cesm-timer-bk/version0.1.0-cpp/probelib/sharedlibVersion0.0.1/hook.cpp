#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#include <iostream>
#include <stack>

int maxDepthTimeStk = 0;

std::stack<void*> funcTimeStack;
std::stack<void*> timeStack;

extern "C"
void __traceBegin_hook() {
	std::cout << "__traceBegin_hook()" << std::endl;
}

extern "C"
void __traceEnd_hook() {
    std::cout << "__traceEnd_hook()" << std::endl;
	std::cout << "maxDepthTimeStk is " << maxDepthTimeStk << std::endl;
}

extern "C" // if no extern "C", c++会minglo函数名（c++支持重载的底层原理）
void __entr_cpp_hook(void *func, void *caller) {
    funcTimeStack.push(func);
}

extern "C"
void __exit_cpp_hook(void *func, void *caller) {
	maxDepthTimeStk < funcTimeStack.size() ? maxDepthTimeStk = funcTimeStack.size() : NULL;
    funcTimeStack.pop();
}