file(GLOB_RECURSE src CMAKE_CONFIGURE_DEPENDS src/*.c include/*.h)
add_library(timer_static STATIC ${src})
target_include_directories(timer_static PUBLIC include)

target_link_libraries(timer_static PUBLIC timer_shared)


