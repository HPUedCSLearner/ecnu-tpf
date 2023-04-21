#pragma once 

#include<iostream>
#include<fstream>
#include<string>
#include<unordered_map>
#include<memory>

#include<assert.h>

namespace MyUtils
{

class AddrMapName
{
public:
    std::string getFuncName(const std::string& addr);
    bool init();
    void showMap(); // for debug
    AddrMapName(const std::string &filename);
private:
    std::unordered_map<std::string, std::string> m_map;
    std::string m_filename;
    std::ifstream m_fin;
};

}