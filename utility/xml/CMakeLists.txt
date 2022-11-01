add_executable(main)
file(GLOB srcs *.cpp *.h)
message("srcs ${srcs}")
target_sources(main PUBLIC  ${srcs})