#include <stdio.h>

#include "private.h"

void __self__traceBegin() {
    printf("__self__traceBegin\n");
}
void __self__traceEnd() {
    printf("__self__traceEnd\n");
}
void __self__cyg_profile_func_enter(void *func, void *caller) {
    printf("##ENTR: __self__cyg_profile_func_enter\n");
}
void __self__cyg_profile_func_exit(void *func, void *caller) {
    printf("##EXIT: __self__cyg_profile_func_exit\n");
}