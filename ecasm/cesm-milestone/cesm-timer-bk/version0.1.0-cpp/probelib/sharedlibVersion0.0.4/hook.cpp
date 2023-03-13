#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
#include <tuple>

#include "utility/perf_counter.h"
#include "utility/get_date.h"

struct pairt_hash
{
    template<typename T1, typename T2>
    std::size_t operator() (const std::pair<T1, T2>& p) const {
        return std::hash<T1>{}(p.first) ^ std::hash<T2>{}(p.second);
    }
};

using LLD = unsigned long long;
using KEY   = std::pair<void*, void*>;
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
	

	char filename[1024] = "/public1/home/fio_climate_model/zyp/tmp/case036/timerShared/version0.1.0-cpp/out/";
    strcat(filename, get_pid());
    strcat(filename, "__");
    strcat(filename, timesStamp());
    strcat(filename,"_functrace.csv");
    printf("%s\n", filename);
    FILE *fw;
    fw = fopen(filename, "w");
	
	for (const auto &callInfoKey : funcSampleInfo) {
        fprintf(fw, "%p\n%p\n", callInfoKey.first, callInfoKey.first);
        fprintf(fw, ",%d,%lld,%lld\n", std::get<0>(callInfoKey.second), std::get<1>(callInfoKey.second), std::get<2>(callInfoKey.second));
    }
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
	
	KEY key;
	if (funcAddrStack.size() == 1) {
		key = KEY{func, caller};
	} else {
		auto selfAddr = funcAddrStack.top();
		funcAddrStack.pop();
		auto fathAddr = funcAddrStack.top();
		key = KEY{selfAddr, fathAddr};
	}
	
	auto acc_start_time = funcTimeStack.top();   funcTimeStack.pop();
    auto shell_start_time = funcTimeStack.top(); funcTimeStack.pop();
	if(funcSampleInfo.find(key) == funcSampleInfo.end()) {
        funcSampleInfo.insert({key, VALUE{1, acc_end_time - acc_start_time, perf_counter() - shell_start_time}});
    } else {
        std::get<0>(funcSampleInfo[key]) ++;
        std::get<1>(funcSampleInfo[key]) += acc_end_time - acc_start_time;
        std::get<2>(funcSampleInfo[key]) += perf_counter() - shell_start_time;
    }
}