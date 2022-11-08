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

void __profile__input_csv();
#define __DEBUG_ENTER_FUNCNAME__
#define __DEBUG_EXIT_FUNCNAME__
#define __DEBUG_STACK_SIZE__

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
MAP funcSampleInfo;

inline const char *get_funcname(const char *src) {
        int status = 99;
        const char *f = abi::__cxa_demangle(src, nullptr, nullptr, &status);
        return f == nullptr ? src : f;
}

extern "C" void __attribute__((constructor)) traceBegin(void) {}

extern "C" void __attribute__((destructor)) traceEnd(void) {}

extern "C" void __cyg_profile_func_enter(void *func, void *caller) { // 插装函数入口：负责压栈两个时间、防止无线递归
    auto shell_start_time = perf_counter(); // 插桩带壳开始时间探针
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        #ifdef __DEBUG_ENTER_FUNCNAME__
        fprintf(stdout, "enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
        #endif
        if (!get_funcname(info1.dli_sname)) { // 不插装的条件
            return;
        } else {
            if( strstr(get_funcname(info1.dli_sname), "::") ||
                strstr(get_funcname(info1.dli_sname), "cxx") ||
                strstr(get_funcname(info1.dli_sname), "operator new") ||
                strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter") ) return;
        }
    }
    funcTimeStack.push(shell_start_time);
    auto acc_start_time = perf_counter(); // 插桩不带壳开始时间探针
    funcTimeStack.push(acc_start_time);
}

extern "C" void __cyg_profile_func_exit(void *func, void *caller) { // 插装函数入口：负责函数调用关系[callee, caller]、弹栈计算时间、写入磁盘
    auto acc_end_time = perf_counter(); // 插桩不带壳结束时间探针
    Dl_info info1, info2;
    if (dladdr(func, &info1) & dladdr(caller, &info2)) {
        #ifdef __DEBUG_EXIT_FUNCNAME__
        fprintf(stdout, "exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
        #endif
        if (!get_funcname(info1.dli_sname) || !get_funcname(info2.dli_sname)) { // 可能由于编译器版本，或者编译flag，或者平台差异，其实，只用caller有可能出现（null）场景
            return;
        } else {
            if( strstr(get_funcname(info1.dli_sname), "::") ||
                strstr(get_funcname(info1.dli_sname), "cxx") ||
                strstr(get_funcname(info1.dli_sname), "operator new") ||
                strstr(get_funcname(info1.dli_sname), "__cyg_profile_func_enter") ) return;
        }
    }
    auto acc_start_time = funcTimeStack.top();   funcTimeStack.pop();
    auto shell_start_time = funcTimeStack.top(); funcTimeStack.pop();
    std::string cur_func = get_funcname(info1.dli_sname);
    std::string fat_func = get_funcname(info2.dli_sname);

    if(funcSampleInfo.find({cur_func, fat_func}) == funcSampleInfo.end()) {
        funcSampleInfo[{cur_func, fat_func}] = {1, acc_end_time - acc_start_time, perf_counter() - shell_start_time};
    } else {
        std::get<0>(funcSampleInfo[{cur_func, fat_func}]) ++;
        std::get<1>(funcSampleInfo[{cur_func, fat_func}]) += acc_end_time - acc_start_time;
        std::get<2>(funcSampleInfo[{cur_func, fat_func}]) += perf_counter() - shell_start_time;
    }
    #ifdef __DEBUG_STACK_SIZE__
    fprintf(stdout, "timestack size is:%ld\n", funcTimeStack.size());
    #endif
    if (funcTimeStack.size() == 2) {
        __profile__input_csv();
    }
}

void __profile__input_csv()
{
    char filename[1024] = "./functrace.csv";
    FILE *fw;
    fw = fopen(filename, "w");
    for (const auto &callInfoKey : funcSampleInfo) {
        fprintf(fw, "%s <- %s[father] ", callInfoKey.first.first.c_str(), callInfoKey.first.second.c_str());
        fprintf(fw, "%d %lld %lld\n", std::get<0>(callInfoKey.second), std::get<1>(callInfoKey.second), std::get<2>(callInfoKey.second));
    }
}