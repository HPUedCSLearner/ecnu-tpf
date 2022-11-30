
#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#define __DEBUG_PRT__
// #define __DEBGU_DLADDR__

inline const char *get_funcname(const char *src) {
        int status = 99;
        const char *f = abi::__cxa_demangle(src, nullptr, nullptr, &status);
        return f == nullptr ? src : f;
}

extern "C" void __attribute__((constructor)) traceBegin(void) {}

extern "C" void __attribute__((destructor)) traceEnd(void) {}

extern "C" void __cyg_profile_func_enter(void *func, void *caller) {
    // #ifdef __DEBUG_PRT__
    // fprintf(stdout, "##entr %p %p\n", func, caller);
    // #endif

    #ifdef __DEBGU_DLADDR__
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
    #endif
}

extern "C" void __cyg_profile_func_exit(void *func, void *caller) {
    #ifdef __DEBUG_PRT__
    fprintf(stdout, "##exit %p %p\n", func, caller);
    #endif

    #ifdef __DEBGU_DLADDR__
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
    #endif
}