
// main.cpp
#include <cstdio>
#include <vector>
#include <dlfcn.h>

void AA();

void BB() {
    Dl_info info1;
    dladdr(nullptr, &info1);

}

void AA() {
    BB();
}

int main() {
    // std::vector<int> a;
    // a.push_back(3);
    AA();
    BB();
    return 0;
}
