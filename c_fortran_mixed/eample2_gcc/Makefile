all:
	gcc -c sub.c -o sub.o -finstrument-functions
	gcc -c instrfunc.c -o instrfunc.o -finstrument-functions
	gfortran -c main.f90 -o main.o -finstrument-functions
	gfortran -o main.exe main.o sub.o instrfunc.o -finstrument-functions

clean:
	rm *.o *.exe