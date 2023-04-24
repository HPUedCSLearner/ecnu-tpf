rm -rf ./*.o ./*.a ./*.so

mpicc mpiwrapper.c -c -finstrument-functions -o mpiwrapper.o
ar -r libmpiwrapper.a mpiwrapper.o 

gcc -shared -fPIC hook.c mem_pool.c hash_table.c -o libhook.so