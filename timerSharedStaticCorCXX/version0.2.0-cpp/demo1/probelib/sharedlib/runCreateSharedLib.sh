rm -rf ./libprobeImpl.so ./libhook.so
gcc -fPIC -shared probeImpl.c -o libprobeImpl.so
g++ -fPIC -shared hook.cpp -o libhook.so