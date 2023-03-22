file(GLOB_RECURSE src CMAKE_CONFIGURE_DEPENDS src/*.cpp include/*.h)
add_library(timer_shared SHARED ${src})
target_include_directories(timer_shared PUBLIC include)
