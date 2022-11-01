add_executable(main)

aux_source_directory(. srcs)
message("srcs ${srcs}")

add_subdirectory(xmlLib)
target_link_libraries(main xml)

target_sources(main PUBLIC  ${srcs})