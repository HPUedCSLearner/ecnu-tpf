rm -rf ./build
cmake -GNinja -B build
# cmake -B build
cmake --build build
build/main