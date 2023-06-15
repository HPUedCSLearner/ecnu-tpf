#!/bin/bash

k_start=16
k_end=1024

k_blocksize=16

echo "result=["
echo -e "%m\t%n\t%k\t%MY_GFLOPS\t%REF_GFLOPS"
for (( k=k_start; k<=k_end; k+=k_blocksize ))
do
    ./a.out     $k $k $k 
done
echo "];"

