#include <perf/bridge.h>
#include <perf/timerImp.h>


void __self__traceBegin() {
    __traceBegin_hook();
}
void __self__traceEnd() {
    __traceEnd_hook();
}
void __self__cyg_profile_func_enter(void *func, void *caller) {
    // __entr_cpp_hook(func, caller);
}
void __self__cyg_profile_func_exit(void *func, void *caller) {
    // __exit_cpp_hook(func, caller);
}


void __self__push_moduleid(int moduId) {
	// push_moduleid(moduId);
}
void __self__pop_moduleid() {
	// pop_moduleid();
}