	gcc -c c.c -o c.o -finstrument-functions
	gfortran -c fortran.f90 -o fortran.o -finstrument-functions
	gfortran -o test fortran.o c.o -L./timing_probe4/libprobeso -lfinstrument