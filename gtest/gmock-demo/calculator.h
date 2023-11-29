// calculator.h
class Calculator {
public:
    virtual ~Calculator() {}
    virtual int Add(int a, int b) const = 0;
};
