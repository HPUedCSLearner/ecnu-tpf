// test_math.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "math.h"

class MockCalculator : public Calculator {
public:
    MOCK_CONST_METHOD2(Add, int(int a, int b));
};

TEST(MathTest, AddNumbers) {
    MockCalculator mockCalculator;  // 创建 Mock 对象

    Math math(&mockCalculator);

    // 设置期望调用
    EXPECT_CALL(mockCalculator, Add(2, 3))
        .WillOnce(::testing::Return(5));

    // 执行被测试的函数
    int result = math.AddNumbers(2, 3);

    // 验证结果
    EXPECT_EQ(result, 5);
}



// 一个简单的测试主函数
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
