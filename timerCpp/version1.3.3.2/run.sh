rm -rf ./*.o ./*.out ./main ./*core*
g++ -c hook.cpp && ar -r libhook.a hook.o
#g++ main.cpp -o main hook.o  -g -finstrument-functions -ldl -rdynamic -no-pie
# gcc main.cpp  -g -finstrument-functions -L/home/maple/myplace/github/ecnu-tpf/timerCpp/version1.3.3.2/ -lhook -lstdc++  -ldl -rdynamic -no-pie -o main 
gcc test.c  -g -finstrument-functions -L/home/maple/myplace/github/ecnu-tpf/timerCpp/version1.3.3.2/ -lhook -lstdc++  -ldl -rdynamic -no-pie -o main 
./main

rm -rf ./*.o ./*.out