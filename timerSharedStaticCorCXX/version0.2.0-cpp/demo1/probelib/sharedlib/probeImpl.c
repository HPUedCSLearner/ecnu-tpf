#include <stdio.h>

#include "private.h"
#include "hook.h"

void __self__traceBegin() {
    printf("__self__traceBegin\n");
}
void __self__traceEnd() {
    printf("__self__traceEnd\n");
}
void __self__cyg_profile_func_enter(void *func, void *caller) {
     __entr_cpp_hook(func, caller);
}
void __self__cyg_profile_func_exit(void *func, void *caller) {
    __exit_cpp_hook(func, caller);
}