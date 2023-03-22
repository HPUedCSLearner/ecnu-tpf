#pragma once

namespace MyUtils
{
    
class NonCopyable
{
protected:
NonCopyable() = default;
~NonCopyable() = default;
NonCopyable(const NonCopyable& rhs) = delete;
NonCopyable& operator=(const NonCopyable& rhs) = delete;
};

}