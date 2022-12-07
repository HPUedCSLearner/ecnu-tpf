rm -rf ./a.out libmax.so timer.o

gcc -fPIC -shared -o libmax.so max.c




gcc -c timer/timer.c
ar -r timer/libtimer.a timer.o


gcc test.c -L. -lmax -g -finstrument-functions -L./timer -ltimer

ldd a.out

LD_LIBRARY_PATH=. ./a.out