

#### 课件链接：
* 源地址：https://github.com/parallel101/course
* 第一节课：https://www.kdocs.cn/l/cvrPbu4kDR0H?f=301
* 第二节课：https://kdocs.cn/l/ckrNBtOEAJPw?f=301
* CMAKE-COOK: https://www.bookstack.cn/read/CMake-Cookbook/README.md
* 


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