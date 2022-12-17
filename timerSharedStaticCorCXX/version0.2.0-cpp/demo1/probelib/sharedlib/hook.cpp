#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

inline const char *get_funcname(const char *src) {
        int status = 99;
        const char *f = abi::__cxa_demangle(src, nullptr, nullptr, &status);
        return f == nullptr ? src : f;
}

extern "C"
void __traceBegin_hook() {
}

extern "C"
void __traceEnd_hook() {
    
}

extern "C" // if no extern "C", c++会minglo函数名（c++支持重载的底层原理）
void __entr_cpp_hook(void *func, void *caller) {
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
}

extern "C"
void __exit_cpp_hook(void *func, void *caller) {
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
}