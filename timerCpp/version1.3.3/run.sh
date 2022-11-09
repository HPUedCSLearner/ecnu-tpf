rm -rf ./*.o ./*.out ./main ./*core*
g++ -c hook.cpp && ar -r libhook.a hook.o
#g++ main.cpp -o main hook.o  -g -finstrument-functions -ldl -rdynamic -no-pie
gcc main.c -o main  -g -finstrument-functions -lhook -lstdc++ -L.  -ldl -rdynamic -no-pie
./main

rm -rf ./*.o ./*.out