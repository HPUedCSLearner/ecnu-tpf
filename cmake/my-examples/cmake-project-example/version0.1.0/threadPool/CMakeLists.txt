file(GLOB_RECURSE srcs CMAKE_CONFIGURE_DEPENDS   src/*.cpp include/*.h)
add_executable(main ${srcs})
target_include_directories(main PUBLIC include)
