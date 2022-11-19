rm -rf ./*.o ./*.out ./main ./*core*
g++ -shared -fPIC hook.cpp -o libhook.so
#g++ main.cpp -o main hook.o  -g -finstrument-functions -ldl -rdynamic -no-pie
gcc main.c  -g -finstrument-functions -L/home/maple/myplace/github/ecnu-tpf/timerCpp/version1.3.3.1/ -lhook -lstdc++  -ldl -rdynamic -no-pie -o main 
./main

rm -rf ./*.o ./*.out