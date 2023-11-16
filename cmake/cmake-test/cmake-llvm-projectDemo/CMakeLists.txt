cmake_minimum_required(VERSION 3.12)

project(cmake-llvm-demo)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_GENERATOR "make")

message(STATUS "============================================")
message(STATUS "====CMAKE: hello this is cmake-llvm-demo====")
message(STATUS "============================================")

message(STATUS "This is SOURCE dir " ${PROJECT_SOURCE_DIR})
message(STATUS "This is BINARY dir " ${PROJECT_BINARY_DIR})

set(EXECUTABLE_OUTPUT_PATH myCmakeBuild)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")


find_package(LLVM REQUIRED)
include_directories(${LLVM_INCLUDE_DIRS})

message(STATUS "============================================")
message(STATUS "LLVM_INCLUDE_DIRS: ${LLVM_INCLUDE_DIRS}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")
message(STATUS "============================================")

llvm_map_components_to_libnames(llvm_all ${LLVM_TARGETS_TO_BUILD} Passes ExecutionEngine MCJIT)
message(STATUS "llvm_all: ${llvm_all}")


add_executable(a.out main.cpp)
target_link_libraries(a.out ${llvm_all})