rm -rf ./build ./core* ./*csv mainAssemble.txt

cmake -B build
cmake --build build

build/main


bash func_trace.sh build/main out_time.csv trace_out.txt

# objdump -ld build/main > mainAssemble.txt