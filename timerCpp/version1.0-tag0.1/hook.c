
#include <stdio.h>
#include <dlfcn.h>

void __attribute__((constructor)) traceBegin(void) {}

void __attribute__((destructor)) traceEnd(void) {}

void __cyg_profile_func_enter(void *func, void *caller) {
    Dl_info info1, info2;
    // if (dladdr(func, &info1) & dladdr(caller, &info2)) {
    //     fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    // }
}

void __cyg_profile_func_exit(void *func, void *caller) {
    Dl_info info1, info2;
    // if (dladdr(func, &info1) & dladdr(caller, &info2)) {
    //     fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    // }
}