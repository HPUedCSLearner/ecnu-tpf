	gcc -c c.c -o c.o
	gfortran -c fortran.f90 -o fortran.o
	gcc -o test fortran.o c.o