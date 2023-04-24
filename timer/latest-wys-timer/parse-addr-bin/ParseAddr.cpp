#include "ParseAddr.hpp"




using namespace MyUtils;

ParseAddr::ParseAddr(const std::shared_ptr<AddrMapName>& mapPtr, const std::string& filename)
:m_funcMapPtr(std::move(mapPtr)), m_filename(std::move(filename))
{}

bool ParseAddr::parse()
{
    m_fin.open(m_filename, std::ios::in);
    if (!m_fin.is_open()) {
        std::cerr << "open file " << m_filename << "Error" << std::endl;
        return false;
    }

    std::string s1;
    while(m_fin >> s1) {
        std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;
    }

    return true;
}

bool ParseAddr::parseToFile(const std::string filename)
{
    std::ofstream fout;
    fout.open(filename, std::ios::out | std::ios::trunc);
    if (!fout.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return false;
    }

    m_fin.open(m_filename, std::ios::in);
    if (!m_fin.is_open()) {
        std::cerr << "open file " << m_filename << "Error" << std::endl;
        return false;
    }

    std::string s1, s2, s3, s4, s5;
    while(m_fin >> s1 >> s2 >> s3 >> s4 >> s5) {
        // fout << m_funcMapPtr->getFuncName(s1) << std::endl;
        fout << m_funcMapPtr->getFuncName(s1) + " "
             << m_funcMapPtr->getFuncName(s2) + " "
             << m_funcMapPtr->getFuncName(s3) + " "
             << m_funcMapPtr->getFuncName(s4) + " "
             << m_funcMapPtr->getFuncName(s5) + " "
             << std::endl;
    }

    m_fin.close();
    fout.close();

    return true;

}