rm -rf ./*.o ./*.out ./main
g++ -shared -fPIC AddrMap.cpp hook.cpp -o libhook.so
# gcc main.c -o main  -g -finstrument-functions -L. -lhook -lstdc++ -L.  -ldl -rdynamic -no-pie
g++  main.cpp -o main  -g -finstrument-functions -L. -lhook -lstdc++ -L.  -ldl -rdynamic -no-pie
export LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH
./main

rm -rf ./*.o ./*.out 