file(GLOB srcs CONFIGURE_DEPENDS *.cpp *.h)
message("srcs :  ${srcs}")

add_library(xml STATIC  ${srcs})
# add_library(xml SHARED  ${srcs})
# add_library(xml OBJECT  ${srcs})