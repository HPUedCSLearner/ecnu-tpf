#pragma once

#include <stdint.h>
#include <string>

namespace processId {

class ProcessId {
public:
static std::string getThreadId();
static std::string getProcessPid();
static std::string getProcessPpid();

};

}