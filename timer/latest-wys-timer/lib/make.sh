rm -rf ./*.o ./*.a

gcc *.c -c
ar -r libhook.a *.o