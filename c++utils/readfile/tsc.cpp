#include "tsc.h"

#include <thread>
#include <future>
#include <sstream>
#include <functional>

namespace MyUtils {

uint64_t TSC::getTsc()
{
    uint32_t lo, hi;
    // take time stamp counter, rdtscp does serialize by itself, and is much cheaper than using CPUID
    __asm__ __volatile__ (
        "rdtscp" : "=a"(lo), "=d"(hi)
        );
    return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}

std::string TSC::getConstCpuHz()
{
    std::stringstream ss;
    ss << "this cpu constant frequence is :" << static_cast<double>(getAvrgOneSecondTsc()) / 1e9 << "GHz";
    return ss.str();
}

uint64_t TSC::getAvrgOneSecondTsc()
{
    std::future<uint64_t> f1 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f2 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f3 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f4 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f5 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f6 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f7 = std::async(std::launch::async, TSC::getOneSecondTsc);
    std::future<uint64_t> f8 = std::async(std::launch::async, TSC::getOneSecondTsc);
    return (f1.get() + f2.get() + f3.get() + f4.get() + f5.get() + f6.get() + f7.get() + f8.get()) / 8;
}

uint64_t TSC::getOneSecondTsc()
{
    auto tick1 = TSC::getTsc();
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    auto tick2 = TSC::getTsc();
    return (tick2 - tick1) * 2;
}

uint64_t TSC::getOneNanoTsc() // 测量的东西越小，误差越大
{
    auto tick1 = TSC::getTsc();
    std::this_thread::sleep_for(std::chrono::nanoseconds(100));
    auto tick2 = TSC::getTsc();
    return (tick2 - tick1) / 100;
}

}