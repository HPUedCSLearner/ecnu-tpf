#pragma once
#include <string>



namespace utility {
namespace xml {

class Value {
public:
    Value();
    Value(const bool value);
    Value(const int value);
    Value(const double value);
    Value(const char * value);
    Value(const std::string value);

private:
    std::string m_value;
};
}
} // namespace utility
