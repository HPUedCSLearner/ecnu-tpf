#pragma once 

#include<iostream>
#include<fstream>
#include<string>
#include<unordered_map>
#include<memory>

#include<assert.h>


#include "AddrMap.hpp"

namespace MyUtils
{

class ParseAddr
{
public:
    ParseAddr(const std::shared_ptr<AddrMapName>& mapPtr, const std::string& filename);
    bool parse();
    bool parseToFile(const std::string filename);
private:
    ParseAddr();
private:
    std::ifstream m_fin;
    std::string m_filename;
    std::shared_ptr<AddrMapName> m_funcMapPtr;
};


}