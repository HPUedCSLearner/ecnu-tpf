rm -rf ./build ./core* ./*csv 

cmake -B build
cmake --build build

build/main

objdump -ld build/main > mainAssemble.txt