export LD_LIBRARY_PATH=/home/tmpDevDir/ecnu-tpf/timer/latest-wys-timer/lib:$LD_LIBRARY_PATH
rm -rf ./a.out
mpic++ testMpi.cpp -finstrument-functions -no-pie  -g -Llib -lmpiwrapper -lhook
./a.out