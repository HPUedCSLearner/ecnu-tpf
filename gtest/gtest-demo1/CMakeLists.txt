cmake_minimum_required(VERSION 3.10)
project(MyProject)

# 添加可执行文件
add_executable(main main.cpp)

# 添加测试可执行文件
add_executable(tests test.cpp)

# 查找 GTest 库
find_package(GTest REQUIRED)

# 包含 GTest 头文件目录
include_directories(${GTEST_INCLUDE_DIRS})

# 链接 GTest 库和线程库到测试文件
target_link_libraries(tests PRIVATE ${GTEST_BOTH_LIBRARIES} pthread)
