
CC = mpicc  -no-pie

LIBS = -lstdc++ -ldl


mydemo: mydemo.o timer.o mpiwrapper.o mpiwrapper_f.o
	${CC} -o mydemo mydemo.o timer.o mpiwrapper.o mpiwrapper_f.o ${LIBS}

timer.o: timer.c
	-${CC} -c -o $@ $<

# mydemo.o: test.c
mydemo.o: mydemo.c
	$(CC) -g -finstrument-functions -c -o $@ $<

mpiwrapper.o: mpiwrapper.c
	-${CC} -g -finstrument-functions -c -o $@ $<

mpiwrapper_f.o: mpiwrapper_f.c
	-${CC} -g -finstrument-functions -c -o $@ $<


.PHONY:cl

cl:
	-rm *.o

run :
	mpirun -np 2 ./mydemo
	sh func_trace.sh mydemo ./out/2_time.csv ./out/func2.out
	sh func_trace.sh mydemo ./out/1_time.csv ./out/func1.out