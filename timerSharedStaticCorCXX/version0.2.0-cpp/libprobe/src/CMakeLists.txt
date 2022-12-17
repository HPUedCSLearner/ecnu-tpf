set(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -g")

cmake_minimum_required(VERSION 3.15)
project(generateInstrumentProbeLie LANGUAGES C)
add_library( instruProbe STATIC timer.c mpiwrapper.c)
target_include_directories(instruProbe PUBLIC ../utility)