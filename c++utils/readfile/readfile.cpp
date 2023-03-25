#include "readfile.h"

#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>

#include <iostream>

namespace MyUtils
{

ReadFile::ReadFile(const std::string &filename) : m_filename(filename) {}

bool ReadFile::init()
{
    m_fin.open(m_filename, std::ios::in);
    if (!m_fin.is_open()) {
        std::cerr << "open file " << m_filename << "Error" << std::endl;
        return false;
    }

    std::string s1, s2;
    while (m_fin >> s1 >> s2) {
        m_map.emplace(s1, s2);
    }
    std::cout << "init done, map size is " << m_map.size() << std::endl;
    m_fin.close();

    initBaseInfo();

    return true;
}
void ReadFile::initBaseInfo()
{
    std::string pid, ppid;
    pid = std::move(std::to_string(getpid()));
    ppid = std::move(std::to_string(getppid()));
    m_map["pid"] = pid;
    m_map["ppid"] = ppid;
}
void ReadFile::showMap()
{
    for (auto & item : m_map) {
        std::cout << item.first << " " << item.second << std::endl;
    }
    std::cout << "this map size is " << m_map.size() << std::endl;
}

const std::string& ReadFile::getValue(const std::string& key)
{
    if (m_map.size() == 0) {
        std::cerr << "map data is zero, can not output value" << std::endl;
        return key; // 没有的话，我们还是返回传进来的值
    }
    if (m_map.find(key) == m_map.end()) {
        std::cerr << "map has not this key, can not output value" << std::endl;
        return key; // 没有的话，我们还是返回传进来的值
    }
    return m_map[key];
}

const std::string& ReadFile::operator[](const std::string& key)
{
    return getValue(key);
}

}