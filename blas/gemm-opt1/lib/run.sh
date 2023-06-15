# cd lib
rm -rf ./*.o
g++ -c *.cpp -g -std=c++11
ar -r libgemm.a *.o
# cd -