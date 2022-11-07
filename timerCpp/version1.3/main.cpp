
// main.cpp
#include <cstdio>
#include <vector>


void BB() {
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
