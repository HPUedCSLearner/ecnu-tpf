# cd lib
rm -rf ./*.o
g++ -c *.cpp -g
ar -r libgemm.a *.o
# cd -