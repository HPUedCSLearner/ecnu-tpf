export PATH=/public1/soft/intel/2017/compilers_and_libraries_2017.7.259/linux/mpi/intel64/bin:$PATH

export PATH=/public1/soft/intel/2017/bin:$PATH




rm -rf ./probe.o ./libprobe.a
mpiicc -c probe.c && ar -r libprobe.a probe.o

