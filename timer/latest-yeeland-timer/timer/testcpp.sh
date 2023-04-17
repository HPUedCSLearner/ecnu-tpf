mpic++ test.cpp -c -finstrument-functions
mpic++ test.o mpiwrapper*.o timer.o -no-pie
./a.out
sh func_trace.sh a.out  ./out/1_time.csv ./out/func1.out
