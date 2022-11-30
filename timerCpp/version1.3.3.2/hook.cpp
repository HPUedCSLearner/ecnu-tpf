// 方向一：避免使用C++ 的模板函数
// 方向二：解决使用C++ 的模板函数的问题

// 所取方向：解决并且使用C++ 的模板函数的问题

// 使用hash MAP 存储调用的关系O（1），（可以事先分配一定的空间，并且使用又值引用，可以提高性能，减小开销）

// __cyg_profile_func_enter 把这个不插装，
// 妙用一：就可以打破环形调用，避免segment falst
// 妙用二：就可以打破环形调用，甚至可以测量我们探针里面使用过的接口
/*


假设，我们的探针实现里面使用过了perf_counter()这个接口，并且被插装的程序里面也有这个perf_counter()这个接口：
当 main -> perf_counter()
perf_counter() -> __cyg_profile_func_enter()
__cyg_profile_func_enter() -> perf_counter()
return
perf_counter() -> __cyg_profile_func_exit()
return

可以参照一下实践，对以上进行分析：
##enter func: main father: (null)
INENTER timestack size is:2
##enter func: perf_counter father: main
INENTER timestack size is:4
##exit func: perf_counter father: main
INEXIT timestack size is:2
##exit func: main father: (null)
INEXIT timestack size is:0

—————————— > [可以用layout asm 看了本文件里面的perf_counter使用c++的那种符号，所以不会有问题]
那么，如果我们用llvm混淆（不一定用llvm）了我们的插装代码的符号表，理论上就可以插装任何函数

-> 分析不出来了吧，还是老老实实加上 void  __attribute__((no_instrument_function))算了

-> 如果可以分析出来，就分析一下，直接给这玩意儿插装__cyg_profile_func_enter，如果分析不出来了，可以直接时间一下试试

*/
#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>
#include <string.h>
#include <unistd.h>
#include "perf_counter.h"

#include <functional>
#include <string>
#include <unordered_map>
#include <tuple>
#include <stack>

#define __DEBUG_FUNCNAME__

#ifdef __DEBUG_FUNCNAME__
#include <dlfcn.h>
#endif


char timestamp[32];
const char* timesStamp();
char _pid[100] = {"\0"};
const char* get_pid();

void __profile__input_csv();
#define __DEBUG_ENTER_FUNCNAME__
// #define __DEBUG_EXIT_FUNCNAME__
// #define __DEBUG_STACK_SIZE__

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
        fprintf(stdout, "##enter func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
        #endif
        std::string callee(get_funcname(info1.dli_sname)); // 不插装的条件
        if (callee.find("::") != std::string::npos || 
            callee.find("cxx") != std::string::npos ||
            callee.find("operator new") != std::string::npos ||
            callee.find("__cyg_profile_func_enter") != std::string::npos) return;
    }
    funcTimeStack.push(shell_start_time);
    auto acc_start_time = perf_counter(); // 插桩不带壳开始时间探针
    funcTimeStack.push(acc_start_time);
    #ifdef __DEBUG_STACK_SIZE__
    fprintf(stdout, "INENTER timestack size is:%ld\n", funcTimeStack.size());
    #endif
}

extern "C" void __cyg_profile_func_exit(void *func, void *fatherFunc) { // 插装函数入口：负责函数调用关系[callee, caller]、弹栈计算时间、写入磁盘
    auto acc_end_time = perf_counter(); // 插桩不带壳结束时间探针
    Dl_info info1, info2;
    std::string callee, caller;
    if (dladdr(func, &info1) & dladdr(fatherFunc, &info2)) {
        #ifdef __DEBUG_EXIT_FUNCNAME__
        fprintf(stdout, "##exit func: %s father: %s\n", get_funcname(info1.dli_sname), get_funcname(info2.dli_sname));
        #endif
        callee = std::string(get_funcname(info1.dli_sname)); // 不插装的条件
        if (callee.find("::") != std::string::npos ||
            callee.find("cxx") != std::string::npos ||
            callee.find("operator new") != std::string::npos ||
            callee.find("__cyg_profile_func_exit") != std::string::npos) return;
        // 可能由于编译器版本，或者编译flag，或者平台差异，其实，只用caller有可能出现（null）场景
        get_funcname(info2.dli_sname) == nullptr ? caller = std::string("null") : caller = std::string(get_funcname(info2.dli_sname));

    }
    auto acc_start_time = funcTimeStack.top();   funcTimeStack.pop();
    auto shell_start_time = funcTimeStack.top(); funcTimeStack.pop();

    if(funcSampleInfo.find({callee, caller}) == funcSampleInfo.end()) {
        funcSampleInfo[{callee, caller}] = {1, acc_end_time - acc_start_time, perf_counter() - shell_start_time};
    } else {
        std::get<0>(funcSampleInfo[{callee, caller}]) ++;
        std::get<1>(funcSampleInfo[{callee, caller}]) += acc_end_time - acc_start_time;
        std::get<2>(funcSampleInfo[{callee, caller}]) += perf_counter() - shell_start_time;
    }
    #ifdef __DEBUG_STACK_SIZE__
    fprintf(stdout, "INEXIT timestack size is:%ld\n", funcTimeStack.size());
    #endif
    if (funcTimeStack.size() == 0) {
        __profile__input_csv();
    }
}

void __profile__input_csv()
{
    char filename[1024] = "./";
    strcat(filename, get_pid());
    strcat(filename, "_");
    strcat(filename, timesStamp());
    strcat(filename,"_functrace.csv");
    printf("%s\n", filename);
    FILE *fw;
    fw = fopen(filename, "w");
    for (const auto &callInfoKey : funcSampleInfo) {
        fprintf(fw, "%s <- %s[father] ", callInfoKey.first.first.c_str(), callInfoKey.first.second.c_str());
        fprintf(fw, "%d %lld %lld\n", std::get<0>(callInfoKey.second), std::get<1>(callInfoKey.second), std::get<2>(callInfoKey.second));
    }
}

const char* get_pid() {
	pid_t current_id;
	current_id = getpid();
	sprintf(_pid, "%d", current_id);
	return _pid;
}



const char* timesStamp()
{
    time_t ticks = time(NULL);
    struct tm* ptm = localtime(&ticks);
    memset(timestamp, 0, sizeof(timestamp));
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d-%H-%M-%S", ptm);
    return timestamp;
}