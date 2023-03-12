file(GLOB_RECURSE src CMAKE_CONFIGURE_DEPENDS src/*.cpp include/*.h)
add_library(utiles STATIC ${src})
target_include_directories(utiles PUBLIC include)
