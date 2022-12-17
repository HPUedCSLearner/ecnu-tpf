rm -rf ./probe.o ./libprobe.a
gcc -c probe.c && ar -r libprobe.a probe.o