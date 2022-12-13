rm -rf ./libprobeImpl.so
gcc -fPIC -shared probeImpl.c -o libprobeImpl.so