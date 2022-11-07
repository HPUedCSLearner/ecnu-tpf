// 方向一：避免使用C++ 的模板函数
// 方向二：解决使用C++ 的模板函数的问题



#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>
#include <string.h>
#include "perf_counter.h"

inline const char *get_funcname(const char *src) {
        int status = 99;
        const char *f = abi::__cxa_demangle(src, nullptr, nullptr, &status);
        return f == nullptr ? src : f;
}

extern "C" void __attribute__((constructor)) traceBegin(void) {}

extern "C" void __attribute__((destructor)) traceEnd(void) {}

extern "C" void __cyg_profile_func_enter(void *func, void *caller) {
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        // if(strstr(get_funcname(info1.dli_sname), "##perf_counter") || // 实验算成功的，符合预期的想象
        if(strstr(get_funcname(info1.dli_sname), "perf_counter") ||
           strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter")  ) return;
        fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
    perf_counter();
}

extern "C" void __cyg_profile_func_exit(void *func, void *caller) {
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        // if(strstr(get_funcname(info1.dli_sname), "##perf_counter") ||
        if(strstr(get_funcname(info1.dli_sname), "perf_counter") ||
           strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter")  ) return;
        fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
}