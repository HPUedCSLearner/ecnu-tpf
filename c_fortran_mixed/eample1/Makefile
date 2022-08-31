all:
	gcc -c sub.c -o sub.o
	gfortran -c main.f90 -o main.o 
	gfortran -o main.exe main.o sub.o

clean:
	rm *.o *.exe