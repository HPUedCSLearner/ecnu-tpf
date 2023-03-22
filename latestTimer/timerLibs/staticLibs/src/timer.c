#include <perf/bridge.h>

void __attribute__((constructor)) traceBegin(void) {
    __self__traceBegin();
}

void __attribute__((destructor)) traceEnd(void) {
    __self__traceEnd();
}

void __cyg_profile_func_enter(void *func, void *caller) {
    __self__cyg_profile_func_enter(func, caller);
}

void __cyg_profile_func_exit(void *func, void *caller) {
    __self__cyg_profile_func_exit(func, caller);
}

void push_moduleid_(int *moduId) {
	__self__push_moduleid(*moduId);
}

void pop_moduleid_() {
	__self__pop_moduleid();
}