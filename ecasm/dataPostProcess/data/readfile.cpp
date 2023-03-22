#include<iostream>
#include<fstream>
#include<string>
#include<unordered_map>
#include<memory>

#include<assert.h>


// 断言
// 用例
// 写文件

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

    // m_fin >> s1;
    // std::cout << s1 << std::endl;
    // std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;
    // m_fin >> s1;
    // std::cout << s1 << std::endl;
    // std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;
    // m_fin >> s1;
    // std::cout << s1 << std::endl;
    // std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;
    // m_fin >> s1;
    // std::cout << s1 << std::endl;
    // std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;
    // m_fin >> s1;
    // std::cout << s1 << std::endl;
    // std::cout << m_funcMapPtr->getFuncName(s1) << std::endl;

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

    std::string s1;
    while(m_fin >> s1) {
        fout << m_funcMapPtr->getFuncName(s1) << std::endl;
    }
    m_fin.close();
    fout.close();

    return true;

}
std::string filename {"./addFuncName.txt.txt"};
void example1()

{
    std::ifstream fin;
    fin.open(filename, std::ios::in);
    if (!fin.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
        return;
    }

    std::string s1, s2;
    while (fin >> s1 >> s2) {
        std::cout << s1 << " " << s2 << std::endl;
    }
}

void example2() {
    // auto addrMapNamePtr = std::make_shared<AddrMapName>("./addFuncName.txt.txt");
    auto addrMapNamePtr = std::make_shared<AddrMapName>("./funcData.txt.txt");
    if (!addrMapNamePtr->init()) {
        return;
    }

    addrMapNamePtr->showMap();

    std::cout << addrMapNamePtr->getFuncName("0x1cb8210") << std::endl;
    assert(addrMapNamePtr->getFuncName("0x1cacf5c") == "vertical_mix_mp_init_vertical_mix_");
    assert(addrMapNamePtr->getFuncName("0x1cb1781") == "vertical_mix_mp_vmix_coeffs_");
    assert(addrMapNamePtr->getFuncName("0x1cb3ffa") == "vertical_mix_mp_vdifft_");
    assert(addrMapNamePtr->getFuncName("0x1cb5b00") == "vertical_mix_mp_vdiffu_");
    assert(addrMapNamePtr->getFuncName("0x1cc1840") == "vertical_mix_mp_convad_");
    assert(addrMapNamePtr->getFuncName("0x1cc3630") == "vmix_const._");

    assert(addrMapNamePtr->getFuncName("0x1cc3630") != "vertical_mix_mp_convad_._");

    assert(addrMapNamePtr->getFuncName("0x1cc3630adf") != "vertical_mix_mp_convad_._");
    assert(addrMapNamePtr->getFuncName("0x1cc3630adf") == "OUT PUT FUN NAME ERROR");
}

void example3() {
    // auto addrMapNamePtr = std::make_shared<AddrMapName>("./addFuncName.txt.txt");
    auto addrMapNamePtr = std::make_shared<AddrMapName>("./funcData.txt.txt");
    if (!addrMapNamePtr->init()) {
        return;
    }

    std::string parseFilename {"131016__2023-03-17__16-04-11_functrace.csv"};
    auto parsePtr = std::make_shared<ParseAddr>(addrMapNamePtr, parseFilename);

    parsePtr->parse();
}

void example4()
{
    auto addrMapNamePtr = std::make_shared<AddrMapName>("./funcData.txt.txt.txt");
    if (!addrMapNamePtr->init()) {
        return;
    }

    std::string parseFilename {"131015__2023-03-17__16-04-11_functrace.csv"};
    auto parsePtr = std::make_shared<ParseAddr>(addrMapNamePtr, parseFilename);

    parsePtr->parseToFile("./parseToFile.out");    
}

int main()
{
    // example1();
    // example2();
    // example3();
    example4();
    return 0;
}














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
