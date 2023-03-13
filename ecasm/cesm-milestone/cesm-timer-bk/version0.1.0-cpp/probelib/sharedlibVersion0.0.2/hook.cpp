#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
#include <tuple>

#include "utility/perf_counter.h"

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

int maxDepthTimeStk = 0;
int maxDepthAddrStk = 0;

std::stack<LLD> funcTimeStack;
std::stack<void*> funcAddrStack;
MAP funcSampleInfo;



extern "C"
void __traceBegin_hook() {
	std::cout << "__traceBegin_hook()" << std::endl;
}

extern "C"
void __traceEnd_hook() {
    std::cout << "__traceEnd_hook()" << std::endl;
	std::cout << "maxDepthTimeStk is " << maxDepthTimeStk << std::endl;
	std::cout << "maxDepthAddrStk is " << maxDepthAddrStk << std::endl;
}

extern "C"
void __entr_cpp_hook(void *func, void *caller) {
	auto shell_start_time = perf_counter();
    funcAddrStack.push(func);
	funcTimeStack.push(shell_start_time);
	funcTimeStack.push(perf_counter());
}

extern "C"
void __exit_cpp_hook(void *func, void *caller) {
	auto acc_end_time = perf_counter();
	
	maxDepthTimeStk < funcAddrStack.size() ? maxDepthTimeStk = funcAddrStack.size() : NULL;
	maxDepthAddrStk < funcTimeStack.size() ? maxDepthAddrStk = funcTimeStack.size() : NULL;
    funcAddrStack.pop();
	funcTimeStack.pop();
	funcTimeStack.pop();
	
}