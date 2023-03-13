export PATH=/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/bin:$PATH

export PATH=/public1/soft/intel/2017/bin:$PATH


rm -rf ./a.out

export LD_LIBRARY_PATH=probelib/sharedlib
export LD_LIBRARY_PATH=/public1/soft/intel/2017/compilers_and_libraries/linux/lib/intel64:$LD_LIBRARY_PATH

mpiicc test.c -g -finstrument-functions -no-pie -Lprobelib -lprobe -Lprobelib/sharedlib -lprobeImpl -lhook 

./a.out
