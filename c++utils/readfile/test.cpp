#include "readfile.h"
#include "timestamp.h"
#include "tsc.h"

#include <memory>
#include <iostream>


#include <fstream>

void test1()
{
    auto rdfPtr = std::make_shared<MyUtils::ReadFile>("config.txt");
    rdfPtr->init();
    rdfPtr->showMap();
    std::cout << rdfPtr->getValue("profilefile") << std::endl;
}

void test2()
{
    MyUtils::ReadFile rdf("config.txt");
    rdf.init();
    rdf.showMap();
    std::cout << rdf.getValue("profilefile") << std::endl;
    std::cout << rdf["profilefile"] << std::endl; // 测试驱动开发
}

void test3()
{
    auto rdfPtr = std::make_shared<MyUtils::ReadFile>("config.txt");
    rdfPtr->init();
    rdfPtr->showMap();
    // std::cout << rdfPtr->getValue("profilefile") << std::endl;

    // std::cout << (*rdfPtr)["profilefile"] << std::endl;
}

void test4()
{
    std::cout << MyUtils::Utils::timestamp() << std::endl;
    std::cout << MyUtils::Utils::timestamp1() << std::endl;
}

void test5()
{
    std::cout << MyUtils::TSC::getAvrgOneSecondTsc() << std::endl;
    std::cout << MyUtils::TSC::getConstCpuHz() << std::endl;
}


void test6()
{
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;
    std::cout << MyUtils::TSC::getTsc() << std::endl;

}

void test7()
{
    std::cout << MyUtils::TSC::getOneNanoTsc() << std::endl;
    std::cout << MyUtils::TSC::getOneNanoTsc() << std::endl;
    std::cout << MyUtils::TSC::getOneNanoTsc() << std::endl;
    std::cout << MyUtils::TSC::getOneNanoTsc() << std::endl;
    std::cout << MyUtils::TSC::getOneNanoTsc() << std::endl;
    std::cout << MyUtils::TSC::getAvrgOneSecondTsc() << std::endl;
}

void test8()
{
    std::cout << MyUtils::TSC::getTscDiff() << std::endl;
    std::cout << MyUtils::TSC::getTscDiff() << std::endl;
    std::cout << MyUtils::TSC::getTscDiff() << std::endl;
    std::cout << MyUtils::TSC::getTscDiff() << std::endl;
    std::cout << MyUtils::TSC::getTscDiff() << std::endl;
}

void test9()
{
    std::cout << MyUtils::TSC::getTicksPerNano() << std::endl;
    std::cout << MyUtils::TSC::getTicksPerNano() << std::endl;
    std::cout << MyUtils::TSC::getTicksPerNano() << std::endl;
    std::cout << MyUtils::TSC::getTicksPerNano() << std::endl;
    std::cout << MyUtils::TSC::getTicksPerNano() << std::endl;
}

void test10()
{
    test8();
    test9();
}

void test11()
{
    auto rdfPtr = std::make_shared<MyUtils::ReadFile>("a.out.txt.txt.txt");
    rdfPtr->init();
    rdfPtr->showMap();
    std::cout << rdfPtr->getValue("profilefile") << std::endl;
}



void test12() // test for read hex文本数据
{
    std::string filename {"test.txt"};
    std::ifstream ifile;
    ifile.open(filename, std::ios::in);
    if (!ifile.is_open()) {
        std::cerr << "open file " << filename << "Error" << std::endl;
    }
    uint64_t int1;
    std::string str1;
    std::string str2;
    ifile >> str1 >> str2;
    std::cout << str1 << std::endl;
    std::cout << std::atoi(str1.c_str()) << std::endl;
    std::cout << str2 << std::endl;
}

int main()
{
    // test1();
    // test2();
    // test3();
    // test4();
    // test5();
    // test6();
    // test7();
    // test8();
    // test9();
    // test10();
    // test11();
    test12();
    return 0;
}