rm -rf ./a.out
gcc test.c -finstrument-functions -no-pie  -g -Llib -lhook
./a.out