export PATH=/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/bin:$PATH

export PATH=/public1/soft/intel/2017/bin:$PATH


rm -rf ./libprobeImpl.so ./libhook.so
mpiicc  -fPIC -shared probeImpl.c -o libprobeImpl.so
mpiicpc -fPIC -shared hook.cpp -o libhook.so

#cp libprobeImpl.so ../sharedlib
#cp libhook.so      ../sharedlib