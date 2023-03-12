#include <processId/process_id.h>

#include <sstream>
#include <thread>
#include <unistd.h>

namespace processId {

std::string ProcessId::getThreadId() {
    std::stringstream ss;
    ss << std::this_thread::get_id();
    return ss.str();
}
std::string ProcessId::getProcessPid() {
    std::stringstream ss;
    ss << getpid();
    return ss.str();
}
std::string ProcessId::getProcessPpid() {
    std::stringstream ss;
    ss << getppid();
    return ss.str();
}

}