
file(GLOB srcs CONFIGURE_DEPENDS *.cpp *.h)
message("srcs :  ${srcs}")

add_library(json STATIC  ${srcs})
# add_library(json SHARED  ${srcs})
# add_library(json OBJECT  ${srcs})

target_include_directories(main PUBLIC .)