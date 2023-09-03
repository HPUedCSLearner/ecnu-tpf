set(LLVM_LINK_COMPONENTS
  Support
)

add_simplelang_tool(simplelang
  Driver.cpp
)

target_link_libraries(simplelang
  PRIVATE
  simplelangBasic
)
