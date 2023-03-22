#ifndef __CPP_HOOK__
#define __CPP_HOOK__

void __traceBegin_hook();
void __traceEnd_hook();
void __entr_cpp_hook(void *func, void *caller);
void __exit_cpp_hook(void *func, void *caller);

void push_moduleid(int moduId);
void pop_moduleid();

#endif