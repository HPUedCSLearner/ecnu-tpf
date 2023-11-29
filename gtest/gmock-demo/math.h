// math.h
#include "calculator.h"

class Math {
public:
    Math(Calculator* calc) : calculator_(calc) {}

    int AddNumbers(int x, int y) const {
        return calculator_->Add(x, y);
    }

private:
    Calculator* calculator_;
};
