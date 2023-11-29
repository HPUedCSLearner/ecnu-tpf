#include <gtest/gtest.h>

// #include "main.cpp"  // 包含你的源代码文件
int add(int a, int b) {
    return a + b;
}

// 测试 add 函数
TEST(AddFunctionTest, PositiveNumbers) {
    EXPECT_EQ(add(2, 3), 5);
}

TEST(AddFunctionTest, NegativeNumbers) {
    EXPECT_EQ(add(-2, -3), -5);
}

TEST(AddFunctionTest, MixedNumbers) {
    EXPECT_EQ(add(2, -3), -1);
}

// 一个简单的测试主函数
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
