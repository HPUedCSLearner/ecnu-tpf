#include "AddrMap.hpp"

using namespace MyUtils;

AddrMapName::AddrMapName(const std::string &filename) :m_filename(std::move(filename)) {}

bool AddrMapName::init() {
    m_fin.open(m_filename, std::ios::in);
    if (!m_fin.is_open()) {
        std::cerr << "open file " << m_filename << "Error" << std::endl;
        return false;
    }

    m_map.reserve(9000);
    std::string s1, s2;
    while (m_fin >> s1 >> s2) {
        // s1 = "0x" + s1; // 0x前缀
        // m_map.insert({s1, s2});
        m_map.emplace(s1, s2);
        // m_map[s1] = s2;
        // std::cout << s1 << " " << s2 << std::endl;  // 这个是OK的啊
    }
    std::cout << "init done, map size is " << m_map.size() << std::endl;
    return true;
}

void AddrMapName::showMap()
{
    for (auto & item : m_map) {
        std::cout << item.first << " " << item.second << std::endl;
    }
}

std::string AddrMapName::getFuncName(const std::string& addr ) {
    if (m_map.size() == 0) {
        std::cerr << "map data is zero, can not output fun name" << std::endl;
        return {"OUT PUT FUN NAME ERROR"};
    }
    if (m_map.find(addr) == m_map.end()) {
        // std::cerr << "map not this address, can not output fun name" << std::endl;
        // return {"OUT PUT FUN NAME ERROR"};
        return addr; // 没有的话，我们还是返回传进来的值
    }
    return m_map[addr];
}