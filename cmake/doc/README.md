

#### 课件链接：
* 源地址：https://github.com/parallel101/course
* 第一节课：https://www.kdocs.cn/l/cvrPbu4kDR0H?f=301
* 第二节课：https://kdocs.cn/l/ckrNBtOEAJPw?f=301


#### 笔记：
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
```