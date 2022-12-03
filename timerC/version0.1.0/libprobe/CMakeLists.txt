set(TOOLCHAIN_DIR "/usr/bin/")
set(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/mpicc)

set(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -g -finstrument-functions -no-pie  -ldl -rdynamic") # 这边的flags也会作用在链接阶段

cmake_minimum_required(VERSION 3.15)
project(Build_timer_project LANGUAGES C CXX Fortran)

message("PROJECT_NAME:             ${PROJECT_NAME}")
message("PROJECT_SOURCE_DIR:       ${PROJECT_SOURCE_DIR}")
message("PROJECT_BINARY_DIR:       ${PROJECT_BINARY_DIR}")
message("CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")

add_subdirectory(src)
 
add_executable(main testSrcs/test.c)
target_link_libraries(main PUBLIC instruProbe)
