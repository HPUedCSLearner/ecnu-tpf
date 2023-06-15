# ./lib/run.sh
rm -rf a.out
g++ my-self-sample-gemm.cpp -g -Llib -lgemm 
./a.out 64 64 64