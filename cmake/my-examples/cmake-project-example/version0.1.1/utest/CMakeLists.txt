file(GLOB_RECURSE srcs CMAKE_CONFIGURE_DEPENDS   gtestMain.cpp threadPool/*.cpp  utiles/*.cpp include/*.h)
add_executable(gtestMain ${srcs})
# target_include_directories(gtestMain PUBLIC include)

find_package(GTest REQUIRED) # -- Up-to-date: /usr/local/lib/cmake/GTest/GTestConfig.cmake   -- Up-to-date: /usr/local/lib/libgtest.a
target_link_libraries(gtestMain PUBLIC GTest::gtest GTest::gmock)

target_link_libraries(gtestMain PUBLIC utiles) # 要给utiles这个库写单元测试，那么直接连接这个库就可以了（1、public属性可是直接使用其头文件；2、刚好可以链接它）