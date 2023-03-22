file(GLOB_RECURSE srcs CMAKE_CONFIGURE_DEPENDS   *.cpp)
add_executable(main ${srcs})
target_include_directories(main PUBLIC include)

set(CMAKE_BUILD_TYPE DEBUG)

find_package(spdlog REQUIRED)
find_package(RapidJSON REQUIRED)

target_compile_options(main PRIVATE -finstrument-functions)

target_link_libraries(main PRIVATE timer_shared timer_static)
target_link_libraries(main PRIVATE spdlog::spdlog)
