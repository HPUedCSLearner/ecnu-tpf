file(GLOB_RECURSE srcs CMAKE_CONFIGURE_DEPENDS   src/*.cpp include/*.h)
add_executable(main ${srcs})
target_include_directories(main PUBLIC include)

set(CMAKE_BUILD_TYPE DEBUG)

find_package(spdlog REQUIRED)
target_link_libraries(main PRIVATE spdlog::spdlog)
target_link_libraries(main PUBLIC utiles)
