#include "xml.h"

#include <sstream>

using namespace utility::xml;


Value::Value()
{
    m_value = "";
}
Value::Value(const bool value)
{
    value == true ? m_value = "true" : m_value = "false";
}
Value::Value(const int value)
{
    std::stringstream ss;
    ss << value;
    m_value = ss.str();
}
Value::Value(const double value)
{
    std::stringstream ss;
    ss << value;
    m_value = ss.str();
}
Value::Value(const char * value)
{
    Value(std::string(value));
}
Value::Value(const std::string value)
{
    m_value = value;
}

