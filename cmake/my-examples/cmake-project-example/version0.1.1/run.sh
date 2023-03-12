rm -rf ./out* ./build*
cmake -B build -G Ninja && cmake --build build
./build/threadPool/main 
./build/utest/gtestMain


