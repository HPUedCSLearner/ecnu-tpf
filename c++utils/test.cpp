#include "Singleton.h"

#include <iostream>
#include <string>

void testSingleton()
{

struct A
{
    A(const std::string&) { std::cout << "lvalue" << std::endl; }
    A(std::string&& x) { std::cout << "rvalue" << std::endl; }
};

struct B
{
    B(const std::string&) { std::cout << "lvalue" << std::endl; }
    B(std::string&& x) { std::cout << "rvalue" << std::endl; }
};

struct C
{
    C(int x, double y) {}
    void Func() { std::cout << "test" << std::endl; }
};

std::string str {"bb"};
MyUtils::Singleton<A>::Instance(str);
MyUtils::Singleton<B>::Instance(std::move(str));
MyUtils::Singleton<C>::Instance(3, 3.14);

MyUtils::Singleton<C>::GetInstance()->Func();

MyUtils::Singleton<A>::DestoryInstace();
MyUtils::Singleton<B>::DestoryInstace();
MyUtils::Singleton<C>::DestoryInstace();

}

int main()
{
    testSingleton();
    return 0;
}