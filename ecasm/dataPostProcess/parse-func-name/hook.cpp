
#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>
#include <stack>
#include <unordered_map>

#include "AddrMap.hpp"
std::stack<void*> st;
using namespace MyUtils;

extern "C" void __attribute__((constructor)) traceBegin(void);

extern "C" void __attribute__((destructor)) traceEnd(void);

extern "C" void __cyg_profile_func_enter(void *func, void *caller);

extern "C" void __cyg_profile_func_exit(void *func, void *caller);



extern "C" void __attribute__((constructor)) traceBegin(void) {
    auto addrMapNamePtr = std::make_shared<AddrMapName>(std::string("main.terminal"));
    addrMapNamePtr->init();
}

extern "C" void __attribute__((destructor)) traceEnd(void) {
    printf("traceEnd\n");
}

extern "C" void __cyg_profile_func_enter(void *func, void *caller) {
    printf("enter %p\n", func);
    st.push(func);
}

extern "C" void __cyg_profile_func_exit(void *func, void *caller) {
    printf("st.size()\n");
}