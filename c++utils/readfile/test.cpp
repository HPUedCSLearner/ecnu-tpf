#include "readfile.h"
#include "timestamp.h"
#include "tsc.h"

#include <memory>
#include <iostream>

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

int main()
{
    // test1();
    // test2();
    // test3();
    // test4();
    test5();
    test6();
    return 0;
}