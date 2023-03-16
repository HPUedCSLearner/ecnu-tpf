#### 课件链接：

* [小彭老师-并行课-源地址：](https://github.com/parallel101/course)
* 第一节课：[01-学C++从CMake学起 (kdocs.cn)](https://www.kdocs.cn/l/cseylGSYkGVR)
* 第二节课：[11-现代 CMake 进阶指南 (kdocs.cn)](https://www.kdocs.cn/l/ckl5Eq90YFvJ)
* 第三节课：[16-现代 CMake 模块化项目管理指南 (kdocs.cn)](https://www.kdocs.cn/l/cjlXZXtPlPcu)
* [book stack - CMAKE-COOK:](https://www.bookstack.cn/read/CMake-Cookbook/README.md)
* [github-dev-cafe](https://github.com/dev-cafe/cmake-cookbook)
* [官方文档cmake.org/cmake/help/latest](https://cmake.org/cmake/help/latest/)
* [Index of /files/v3.25 (cmake.org)](https://cmake.org/files/v3.25/)

### 现代cmake语法

##### cmake设置语言标准

[CMake 设置语言标准](https://blog.csdn.net/weixin_39766005/article/details/122481172)

```cmake
#启用C++14
set_target_properties(lib
  PROPERTIES
    CXX_STANDARD 14
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE 1
  )


  cmake -DCMAKE_CXX_STANDARD=17 ...
```

上述代码为库设置了CXX_STANDARD 、CXX_EXTENSIONS和CXX_STANDARD_REQUIRED 属性。还设置了POSITION_INDEPENDENT_CODE 属性，以避免在使用一些编译器构建DSO时出现问题。

CXX_STANDARD会设置我们想要的标准。
CXX_EXTENSIONS告诉CMake，只启用 ISO C++ 标准的编译器标志，而不使用特定编译器的扩展。
CXX_STANDARD_REQUIRED指定所选标准的版本。如果这个版本不可用，CMake将停止配置并出现错误。当这个属性被设置为 OFF 时，CMake将寻找下一个标准的最新版本，直到一个合适的标志，这意味着，首先查找 C++ 20，然后是C++17，然后是C++14，然后是C++11 ，然后是 C++98 。

#### 笔记：

```cmake
add_executable()
target_sources()
set()
file()
aux_source_directory()

PUBLIC、GLOB、CONFIGURE_DEPENDS、GLOB_RECURSE、
```

```cmake

11 - 01
add_executable(main main.cpp)


add_executable(main)
target_sources(main PUBLIC main.cpp)


add_executable(main)
target_sources(main PUBLIC main.cpp other.cpp)

add_executable(main)
set(sources main.cpp other.cpp)
target_sources(main PUBLIC ${sources})


add_executable(main)
set(sources main.cpp other.cpp other.h)
target_sources(main PUBLIC ${sources})


add_executable(main)
file(GLOB sources *.cpp *.h)
target_sources(main PUBLIC ${sources})


add_executable(main)
file(GLOB sources CONFIGURE_DEPENDS *.cpp *.h)
target_sources(main PUBLIC ${sources})


add_executable(main)
file(GLOB sources CONFIGURE_DEPENDS *.cpp *.h mylib/*.cpp mylib/*.h)
target_sources(main PUBLIC ${sources})


add_executable(main)
file(GLOB_RECURSE sources CONFIGURE_DEPENDS *.cpp *.h)
target_sources(main PUBLIC ${sources})

add_executable(main)
aux_source_directory(. sources)
aux_source_directory(mylib sources)
target_sources(main PUBLIC ${sources})


11 - 02
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

cmake_minimum_required(VERSION 3.15)
project(hellocmake LANGUAGES CXX)

set(CMAKE_BUILD_TYPE Release)

add_executable(main main.cpp)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

cmake_minimum_required(VERSION 3.15)
project(hellocmake LANGUAGES C CXX)

add_executable(main main.cpp)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


cmake_minimum_required(VERSION 3.15)
project(hellocmake)

message("PROJECT_NAME: ${PROJECT_NAME}")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
message("PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")
message("CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
add_executable(main main.cpp)

add_subdirectory(mylib)

---------------| add_subdirectory()
message("mylib got PROJECT_NAME: ${PROJECT_NAME}")
message("mylib got PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
message("mylib got PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")
message("mylib got CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("mylib got CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.15)
project(hellocmake LANGUAGES NONE)
enable_language(CXX)

add_executable(main main.cpp)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

project(hellocmake LANGUAGES CXX)

add_executable(main main.cpp)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


cmake_minimum_required(VERSION 3.15)
project(hellocmake)

message("PROJECT_NAME: ${PROJECT_NAME}")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
message("PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")
message("CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
add_executable(main main.cpp)

add_subdirectory(mylib)

---------------| add_subdirectory()
project(mylib)

message("mylib got PROJECT_NAME: ${PROJECT_NAME}")
message("mylib got CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message("mylib got CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")
message("mylib got PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
message("mylib got PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")
message("mylib got CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("mylib got CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.15)
project(hellocmake
    DESCRIPTION "A free, open-source, online modern C++ course"
    HOMEPAGE_URL https://github.com/parallel101/course
    )

message("PROJECT_NAME: ${PROJECT_NAME}")
message("PROJECT_DESCRIPTION: ${PROJECT_DESCRIPTION}")
message("PROJECT_HOMEPAGE_URL: ${PROJECT_HOMEPAGE_URL}")
add_executable(main main.cpp)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.15)
project(hellocmake VERSION 0.2.3)

message("PROJECT_NAME: ${PROJECT_NAME}")
message("PROJECT_VERSION: ${PROJECT_VERSION}")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")
message("PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")
message("hellocmake_VERSION: ${hellocmake_VERSION}")
message("hellocmake_SOURCE_DIR: ${hellocmake_SOURCE_DIR}")
message("hellocmake_BINARY_DIR: ${hellocmake_BINARY_DIR}")
add_executable(main main.cpp)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.99)
project(hellocmake LANGUAGES CXX)

message("CMAKE_VERSION: ${CMAKE_VERSION}")
add_executable(main main.cpp)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.99)
project(hellocmake LANGUAGES CXX)

message("CMAKE_VERSION: ${CMAKE_VERSION}")
add_executable(main main.cpp)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmake_minimum_required(VERSION 3.15...3.20)
project(hellocmake LANGUAGES CXX)

message("CMAKE_VERSION: ${CMAKE_VERSION}")
message("CMAKE_MINIMUM_REQUIRED_VERSION: ${CMAKE_MINIMUM_REQUIRED_VERSION}")
add_executable(main main.cpp)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```
