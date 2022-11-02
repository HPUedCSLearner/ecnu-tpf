OPEN_ARRAY=/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/build.slave

oplevel3 = -O2 -w  -std=c++0x -D_WITHOUT_LLVM_ -DSUNWAY    -I/home/export/online1/mdt00/shisuan/swliuyao/oa/lib/armadillo -I/usr/sw/yyzlib/pnetcdf/include -fpermissive -faddress_align=64

FC = mpif90 ${oplevel3} -mieee -faddress_align=64
CC = mpicc -O2 -w -mieee -faddress_align=64

EXT_LIB_LINK = 	-lpnetcdf  -ldl  -Wl,-rpath=${JIT_LIB}

LIBS =  -lstdc++ ${EXT_LIB} ${EXT_LIB_LINK}

FCFLAGS = -Wno-tabs  \
		  -I${OPEN_ARRAY} -g -finstrument-functions \
		  -fbacktrace -ffree-line-length-0 


# %.o: %.c
# 	${CC} ${CFLAGS} -c -o $@ $<


mydemo: mydemo.o timer.o mpiwrapper.o mpiwrapper_f.o
	${FC} -o mydemo mydemo.o mydebug.o timer.o \
	${EXT_LIB_LINK} ${LIBS} -I${OPEN_ARRAY} -L${OPEN_ARRAY} \
	-lgfortran -L. -lopenarray -lm -lm_slave -ldl -lstdc++ -L/usr/sw/yyzlib/pnetcdf/lib -lpnetcdf

timer.o: timer.c
	-${CC} ${CFLAGS} -c -o $@ $<

mydemo.o: mydemo.F90
	$(FC) ${FCFLAGS} -c $< -o $@

mpiwrapper.o: mpiwrapper.c
	-${CC} ${CFLAGS} -g -finstrument-functions -c -o $@ $<

mpiwrapper_f.o: mpiwrapper_f.c
	-${CC} ${CFLAGS} -g -finstrument-functions -c -o $@ $<


.PHONY:clean

clean:
	-rm mydemo.o
	-rm mydemo

run :
	-rm time.out
	-rm func.out
	bsub -I -q q_sw_expr -share_size 7000 -host_stack 4096 -n 1 -cgsp 64 ./mydemo
	sh func_trace.sh mydemo time.out func.out