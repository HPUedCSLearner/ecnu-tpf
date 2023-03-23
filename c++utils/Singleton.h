#pragma once

#include <utility>
#include <iostream>

namespace MyUtils
{

template<typename T>
class Singleton
{
private:
    static T* m_instance;
private:
    Singleton();
    virtual ~Singleton();
    Singleton(const Singleton& rhs);
    Singleton& operator=(const Singleton&rhs);
public:
    template<typename... Args>
    static T* Instance(Args&&... args)
    {
        if (m_instance == nullptr) {
            m_instance = new T(std::forward<Args>(args)...);
        }
        return m_instance;
    }
    static T* GetInstance() {
        if (m_instance == nullptr) {
            throw std::logic_error("fatal error: the instance in not init, please initialize the instace first");
        }
        return m_instance;
    }

    static void DestoryInstace() {
        if (m_instance == nullptr) {
            throw std::logic_error("fatal error: delete ptr of nullprt");
            return;
        }
        delete m_instance;
        m_instance = nullptr;
    }
};

template <typename T>
T* Singleton<T>::m_instance = nullptr;

}