rm -rf ./*.o ./*.out ./main
# g++ -c hook.cpp && ar -r libhook.a hook.o
gcc -c hook.c && ar -r libhook.a hook.o
#g++ main.cpp hook.o  -g -finstrument-functions -ldl -rdynamic -no-pie
gcc main.c -o main  -g -finstrument-functions -lhook -lstdc++ -L.  -ldl -rdynamic -no-pie
./main

rm -rf ./*.o ./*.out ./main