add_executable(main)

aux_source_directory(. srcs)
message("srcs ${srcs}")
# target_include_directories(main json)

add_subdirectory(json)
target_link_libraries(main PUBLIC json)

target_sources(main PUBLIC  ${srcs})