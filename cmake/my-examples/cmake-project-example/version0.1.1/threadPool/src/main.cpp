#include <iostream>
#include <random>
#include <memory>
#include <sstream>

#include <functional>

#include<threadPool/threadPool.h>
#include<spdlog/spdlog.h>

#include<processId/process_id.h>
#include<perf/perf_counter.h>



std::random_device rd; // 真实随机数产生器
std::mt19937 mt(rd()); //生成计算随机数mt
std::uniform_int_distribution<int> dist(-1000, 1000); //生成-1000到1000之间的离散均匀分布数
auto rnd = std::bind(dist, mt);
// 设置线程睡眠时间
void simulate_hard_computation()
{
    std::this_thread::sleep_for(std::chrono::milliseconds(2000 + rnd()));
}
// 添加两个数字的简单函数并打印结果
void multiply(const int a, const int b)
{
    simulate_hard_computation();
    const int res = a * b;
    // std::cout << a << " * " << b << " = " << res << std::endl;
    spdlog::info("{} * {} = {}", a, b, res);
}
// 添加并输出结果
void multiply_output(int &out, const int a, const int b)
{
    simulate_hard_computation();
    out = a * b;
    // std::cout << a << " * " << b << " = " << out << std::endl;
    spdlog::info("{} * {} = {}", a, b, out);
}
// 结果返回
int multiply_return(const int a, const int b)
{
    simulate_hard_computation();
    const int res = a * b;
    // std::cout << a << " * " << b << " = " << res << std::endl;
    spdlog::info("{} * {} = {}", a, b, res);
    return res;
}

template <typename... Args>
void INFO(Args &&...args)
{
    spdlog::info(std::forward<Args>(args)...);
}

void example()
{
    processId::ProcessId::getProcessPid();
    spdlog::info("[{}] [{}] welcome to example!", processId::ProcessId::getProcessPid(), processId::ProcessId::getThreadId());
    spdlog::error("Some error message with arg: {}", 1);
    
    std::stringstream ss; 
    ss << std::this_thread::get_id() ;
    spdlog::info("thread id: {}", ss.str());

    std::shared_ptr<threadPool::ThreadPool> pool = std::make_shared<threadPool::ThreadPool>(300);
    pool->init();

    // 提交乘法操作，总共30个
    for (int i = 1; i <= 3; ++i) {
        for (int j = 1; j <= 100; ++j)
        {
            pool->submit(multiply, i, j);
        }
    }

    // 使用ref传递的输出参数提交函数
    int output_ref;
    auto future1 = pool->submit(multiply_output, std::ref(output_ref), 5, 6);
    // 等待乘法输出完成
    future1.get();
    std::cout << "Last operation result is equals to " << output_ref << std::endl;


    // 使用return参数提交函数
    auto future2 = pool->submit(multiply_return, 5, 3);
    // 等待乘法输出完成
    int res = future2.get();
    std::cout << "Last operation result is equals to " << res << std::endl;

    pool->shutdown();
}



int main() {
    example();
    return 0;
}