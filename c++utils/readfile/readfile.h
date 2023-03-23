#pragma once

#include <fstream>
#include <string>
#include <unordered_map>

namespace MyUtils
{

class ReadFile
{
public:
ReadFile(const std::string &filename);
bool init();
void showMap();
const std::string& getValue(const std::string& key);
const std::string& operator[](const std::string& key);

protected:
void initBaseInfo();

private:
std::ifstream m_fin;
std::unordered_map<std::string, std::string> m_map;
std::string m_filename;
};


}