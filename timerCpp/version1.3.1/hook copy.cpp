// 方向一：避免使用C++ 的模板函数
// 方向二：解决使用C++ 的模板函数的问题

// 所取方向：解决并且使用C++ 的模板函数的问题

#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>
#include <string.h>
#include "perf_counter.h"

#include <string>
#include <unordered_map>
#include <tuple>
#include <stack>

struct pairt_hash
{
    template<typename T1, typename T2>
    std::size_t operator() (const std::pair<T1, T2>& p) const {
        return std::hash<T1>{}(p.first) ^ std::hash<T2>{}(p.second);
    }
};

using LLD = unsigned long long;
using KEY   = std::pair<std::string, std::string>;
using VALUE = std::tuple<int, LLD, LLD>;
using MAP = std::unordered_map<KEY, VALUE, pairt_hash>;

std::stack<LLD> funcTimeStack;
MAP funcInfo;

inline const char *get_funcname(const char *src) {
        int status = 99;
        const char *f = abi::__cxa_demangle(src, nullptr, nullptr, &status);
        return f == nullptr ? src : f;
}

extern "C" void __attribute__((constructor)) traceBegin(void) {}

extern "C" void __attribute__((destructor)) traceEnd(void) {}

extern "C" void __cyg_profile_func_enter(void *func, void *caller) {
    auto shell_start_time = perf_counter();
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        if(strstr(get_funcname(info1.dli_sname), "perf_counter") ||
           strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter") ||
           strstr(get_funcname(info1.dli_sname), "operator new") ||
           strstr(get_funcname(info1.dli_sname), "::") ) return;
        fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
    funcTimeStack.push(shell_start_time);
    funcTimeStack.push(perf_counter());
}

extern "C" void __cyg_profile_func_exit(void *func, void *caller) {
    auto acc_end_time = perf_counter();
    auto acc_start_time = funcTimeStack.top(); funcTimeStack.pop();
    auto shell_start_time = funcTimeStack.top(); funcTimeStack.pop();
    std::string cur_func, fat_func;
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
        if(strstr(get_funcname(info1.dli_sname), "perf_counter") ||
           strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter") ||
           strstr(get_funcname(info1.dli_sname), "operator new") ||
           strstr(get_funcname(info1.dli_sname), "::") ) return;
        // fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
    }
    cur_func = get_funcname(info1.dli_sname);
    fat_func = get_funcname(info2.dli_sname);

    if(funcInfo.find({cur_func, fat_func}) == funcInfo.end()) {
        funcInfo[{cur_func, fat_func}] = {1, acc_start_time - acc_end_time, shell_start_time - perf_counter()};
    } else {
        std::get<0>(funcInfo[{cur_func, fat_func}]) ++;
        std::get<1>(funcInfo[{cur_func, fat_func}]) += (acc_start_time - acc_end_time);
        std::get<2>(funcInfo[{cur_func, fat_func}]) += (shell_start_time - perf_counter());
    }
}