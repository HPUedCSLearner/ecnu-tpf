#include <string>
#include <unordered_map>
#include <fstream>
#include <iostream>

void readfile()
{
    std::fstream fin;
    std::string filename {"data.csv"};
    fin.open(filename, std::ios::in);
    if (!fin.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return ;
    }
    std::string s1, s2, s3, s4, s5, s6;
    fin >> s1 >>  s2 >>  s3 >>  s4 >>  s5 >> s6;
    std::cout   << s1 << std::endl 
                << s2 << std::endl 
                << s3 << std::endl 
                << s4 << std::endl 
                << s5 << std::endl
                << s6 << std::endl ;
}


void readfile1()
{
    std::fstream fin;
    std::string filename {"data.csv"};
    fin.open(filename, std::ios::in);
    if (!fin.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return ;
    }
    std::string s1, s2;
    int times;
    unsigned long long acctime, shelltime;
    fin >> s1 >>  s2 >>  times >>  acctime >>  shelltime;
    std::cout   << s1 << std::endl 
                << s2 << std::endl 
                << times << std::endl 
                << acctime << std::endl 
                << shelltime << std::endl;
}

void readfile2()
{
    std::fstream fin;
    // std::string filename {"data.csv"};
    std::string filename {"1024_func.out"};
    fin.open(filename, std::ios::in);
    if (!fin.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return ;
    }
    std::string s1, s2;
    int times;
    using LL = unsigned long long;
    LL acctime, shelltime;
    std::unordered_map<std::string, LL> self_func_runtime, son_func_runtime;

    // 聚合 自身运行时间，聚合 孩子运行时间
    while(fin >> s1 >>  s2 >>  times >>  acctime >>  shelltime) {
        // std::cout   << s1 << " "
        //         << s2 << " "
        //         << times << " " 
        //         << acctime << " "
        //         << shelltime << std::endl;
        if (self_func_runtime.find(s1) == self_func_runtime.end()) {
            self_func_runtime.emplace(s1, acctime);
        } else {
            self_func_runtime[s1] += acctime;
        }

        if (son_func_runtime.find(s2) == son_func_runtime.end()) {
            son_func_runtime.emplace(s2, shelltime);
        } else {
            son_func_runtime[s2] += shelltime;
        }
    }
    fin.close();

    // debug 打印聚合时间
    for (const auto& items : self_func_runtime) {
        std::cout << items.first << " " << items.second << std::endl;
    }
    // 函数运行时间 = 自身运行时间 - 孩子运行时间
    for (const auto& items : self_func_runtime) {
        if (son_func_runtime.find(items.first) != son_func_runtime.end()) { // 如果这个函数有 子函数
            self_func_runtime[items.first] -= son_func_runtime[items.first];
        }
    }

    // debug 打印结果
    std::cout << "=================================================" << std::endl;
    for (const auto& items : self_func_runtime) {
        std::cout << items.first << " " << items.second << std::endl;
    }

    // 处理结果写入文件
    std::fstream fout;
    fout.open(filename + ".out", std::ios::out | std::ios::trunc);
    if (!fout.is_open()) {
        std::cerr << "open file " << filename + ".out" << "Error" << std::endl;
        return ;
    }

    for (const auto& items : self_func_runtime) {
        fout << items.first << " " << items.second << std::endl;
    }
    fout.close();

}

void readfile3()
{
    std::fstream fin;
    // std::string filename {"data.csv"};
    std::string filename {"1024_func.out"};
    fin.open(filename, std::ios::in);
    if (!fin.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return ;
    }
    std::string s1, s2;
    int times;
    using LL = unsigned long long;
    LL acctime, shelltime;
    std::unordered_map<std::string, LL> self_func_runtime, son_func_runtime;

    // 聚合 自身运行时间，聚合 孩子运行时间
    while(fin >> s1 >>  s2 >>  times >>  acctime >>  shelltime) {
        if (self_func_runtime.find(s1) == self_func_runtime.end()) {
            self_func_runtime.emplace(s1, acctime);
        } else {
            self_func_runtime[s1] += acctime;
        }

        if (son_func_runtime.find(s2) == son_func_runtime.end()) {
            son_func_runtime.emplace(s2, shelltime);
        } else {
            son_func_runtime[s2] += shelltime;
        }
    }
    fin.close();

    // 函数运行时间 = 自身运行时间 - 孩子运行时间
    for (const auto& items : self_func_runtime) {
        if (son_func_runtime.find(items.first) != son_func_runtime.end()) { // 如果这个函数有 子函数
            self_func_runtime[items.first] -= son_func_runtime[items.first];
        }
    }

    // 处理结果写入文件
    std::fstream fout;
    fout.open(filename + ".out", std::ios::out | std::ios::trunc);
    if (!fout.is_open()) {
        std::cerr << "open file " << filename + ".out" << "Error" << std::endl;
        return ;
    }

    for (const auto& items : self_func_runtime) {
        fout << items.first << " " << items.second << std::endl;
    }
    fout.close();

}

int main()
{
    // readfile();
    // readfile1();
    // readfile2();
    readfile3();
    return 0;
}