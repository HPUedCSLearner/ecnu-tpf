#include <cstdio>
#include <dlfcn.h>
#include <cxxabi.h>

#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
#include <tuple>

#include "utiles/perf_counter.h"
#include "utiles/get_date.h"

const char* moduleName[] {  "module0", "module1", "module2", "module3", "module4", "module5",
						    "module6", "module7", "module8", "module9", "module10",
						    "module11", "module12", "module13", "module14", "module15",
						    "module16", "module17", "module18", "module19", "module20",
							"moudleMain"
						};

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
using MODULE_MAP_INFO = std::unordered_map<const char*, MAP>;

int maxDepthTimeStk = 0;
int maxDepthAddrStk = 0;

std::stack<LLD> funcTimeStack;
std::stack<void*> funcAddrStack;

std::stack<int> moduleStack;

MAP funcSampleInfo;
MODULE_MAP_INFO moduleMapInfo;

void init() {
	std::cout << "in Process id " << get_pid() << " ：probe init() begin" << std::endl;
	int moudleNum = sizeof(moduleName) / sizeof(const char*);
	for (int i = 0; i < moudleNum; ++i) {
		moduleMapInfo.insert({moduleName[i], MAP()});
	}
	moduleStack.push(moudleNum - 1); // 预先加入一个module - main，避免moduleStack为0，访问top()的时候，会crash
	std::cout << "moduleMapInfo.size = " << moduleMapInfo.size() << std::endl;
	std::cout << "in Process id " << get_pid() << " ：probe init() end" << std::endl;
}

extern "C"
void push_moduleid(int moduId) {  // 是否有可能被插装？
	std::cout << "wys: push module id " << moduId << std::endl;
	moduleStack.push(moduId);
}

extern "C"
void pop_moduleid(){
	std::cout << "wys: pop module id " << moduleStack.top() << std::endl;
	moduleStack.pop();
}

extern "C"
void __traceBegin_hook() {
	std::cout << "__traceBegin_hook()" << std::endl;
	init();
}

extern "C"
void __traceEnd_hook() {
    std::cout << "__traceEnd_hook()" << std::endl;
	std::cout << "maxDepthTimeStk is " << maxDepthTimeStk << std::endl;
	std::cout << "maxDepthAddrStk is " << maxDepthAddrStk << std::endl;
	std::cout << "moduleStack size is " << moduleStack.size() << std::endl;
	

	char filename[1024] = "/public1/home/fio_climate_model/zyp/tmp/case036/timerShared/version0.1.0-cpp/out/";
    strcat(filename, get_pid());
    strcat(filename, "__");
    strcat(filename, timesStamp());
    strcat(filename,"_functrace.csv");
    printf("%s\n", filename);
    FILE *fw;
    fw = fopen(filename, "w");

	for (const auto &moduleInfo : moduleMapInfo) {
		fprintf(fw, moduleInfo.first);
		fprintf(fw, ":\n");
		if (moduleInfo.second.size() == 0) {
			continue;
		}
		for (const auto &callInfoKey : moduleInfo.second) {
			fprintf(fw, "%p\n%p\n", callInfoKey.first, callInfoKey.first);
			fprintf(fw, ",%d,%lld,%lld\n", std::get<0>(callInfoKey.second), std::get<1>(callInfoKey.second), std::get<2>(callInfoKey.second));
		}
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
	if (funcAddrStack.size() == 1) { // 如果是主函数了，去其父函数为caller
		key = KEY{func, caller};
	} else {
		auto selfAddr = funcAddrStack.top();
		funcAddrStack.pop();
		auto fathAddr = funcAddrStack.top();
		key = KEY{selfAddr, fathAddr};
	}
	
	
	auto acc_start_time = funcTimeStack.top();   funcTimeStack.pop();
    auto shell_start_time = funcTimeStack.top(); funcTimeStack.pop();
	auto &thisfuncSampleInfo = moduleMapInfo[moduleName[moduleStack.top()]]; // if moduleStack.size() == 0 , would be crash
	if(thisfuncSampleInfo.find(key) == thisfuncSampleInfo.end()) {
        thisfuncSampleInfo.insert({key, VALUE{1, acc_end_time - acc_start_time, perf_counter() - shell_start_time}});
    } else {
        std::get<0>(thisfuncSampleInfo[key]) ++;
        std::get<1>(thisfuncSampleInfo[key]) += acc_end_time - acc_start_time;
        std::get<2>(thisfuncSampleInfo[key]) += perf_counter() - shell_start_time;
    }
}