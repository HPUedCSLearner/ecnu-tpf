#include <functional>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <string>


extern "C" {
void hash_int(int x) {
    std::hash<int> hashInt;
    std::cout << "hash int is : " << hashInt(x) << std::endl;
}

}
