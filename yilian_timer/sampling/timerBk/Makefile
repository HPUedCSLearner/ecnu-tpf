



FLAGS = -Wno-tabs  \
		-g -finstrument-functions \
		-fbacktrace -ffree-line-length-0

lib:timer.o mpiwrapper.o
	mpicc -c timer.c -o timer.o
	#mpicxx -c mpiwrapper.c -o mpiwrapper.o
	ar -r libyiliantimer.a timer.o mpiwrapper.o

	gcc test.c -finstrument-functions -L -lyiliantimer -lstdc++
cl:
	rm -rf *.a *.o
dump:
	objdump -d timer.o > timer.c.assmble.txt
dumpa.out:
	objdump -d a.out > a.out.assmble.txt