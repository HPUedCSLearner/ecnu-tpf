#include "timestamp.h"

#include <chrono>
#include <time.h>
#include <iomanip>
#include <sstream>
#include <stdio.h>
#include <string.h>

using namespace MyUtils;

const std::string Utils::timestamp1()
{
    using namespace std::chrono;
    auto t = system_clock::to_time_t(system_clock::now() + hours(8));
    std::stringstream ss;
    // ss << std::put_time(std::localtime(&t), "%Y-%m-%d.%H.%M.%S"); // 在超算上 编译不过
    return ss.str();
}

const std::string Utils::timestamp()
{
    std::stringstream ss;
    char buf[10] {0};
    time_t now = time(NULL);
    tm* ltm = localtime(&now);
    ss << 1900 + ltm->tm_year << "-";
    ss << 1 + ltm->tm_mon << "-";
    ss << ltm->tm_mday << "(";
    sprintf(buf, "%02d", ltm->tm_hour + 8);
    ss << buf << ".";
    memset(buf, 0, sizeof(buf));
    sprintf(buf, "%02d", ltm->tm_min);
    ss << buf << ".";
    memset(buf, 0, sizeof(buf));
    sprintf(buf, "%02d", ltm->tm_sec);
    ss << buf << ")";
    return ss.str();
}