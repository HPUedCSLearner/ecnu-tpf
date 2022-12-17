#ifndef __PROBLE_IPMl_BRIDGE__
#define __PROBLE_IPMl_BRIDGE__

void __self__traceBegin();
void __self__traceEnd();
void __self__cyg_profile_func_enter(void *func, void *caller);
void __self__cyg_profile_func_exit(void *func, void *caller);

#endif