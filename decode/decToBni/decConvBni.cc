
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>

#include <unordered_map>

using std::vector;
using std::string;
using std::unordered_map;

class ConvertDecBni {
public:
    ConvertDecBni(int a) :num(a) {}
    void resetNum(int a) { num = a; }
    void convert();
    void printVec();
    string printStr();
private:
    vector<int> res;
    int num;
};


class MapDS {
public:
    MapDS(ConvertDecBni *_CDB_prt) :CDB_prt(_CDB_prt) {}
    ~MapDS() { if(CDB_prt) delete CDB_prt; }
    void MapDS_init();
    char toChar(string);
    string toString(char);
private:
    unordered_map<char, string> MapCS;
    unordered_map<string, char> MapSC;
    ConvertDecBni *CDB_prt;
};

void MapDS::MapDS_init() {
    for (int i = 0; i < 128; ++i) {
        CDB_prt->resetNum(i);
        CDB_prt->convert();
        MapCS[i] = CDB_prt->printStr();
        MapSC[CDB_prt->printStr()] = i;
    }
}

char MapDS::toChar(string str) {
    return MapSC[str];
}

string MapDS::toString(char ch) {
    return MapCS[ch];
}

void ConvertDecBni::convert() {
    res.clear();
    while (num) {
        res.push_back(num & 0x01);
        num = (num >> 1);
    }
    std::reverse(std::begin(res), std::end(res));
}

void ConvertDecBni::printVec() {
    for (auto i : res) {
        std::cout << i << " ";
    }
    std::cout << '\r' << std::endl;

}

string ConvertDecBni::printStr() {
    string retV;
    for (auto i : res) {
        retV += std::to_string(i);
    }
    return ("00000000" + retV).substr(retV.length()); // 不足，补零
}

int main() {
    // test for ConvertDecBni
    // int a = 3;
    // ConvertDecBni cvdb(a);
    // cvdb.convert();
    // cvdb.printVec();

    // cvdb.resetNum(64);
    // cvdb.convert();
    // cvdb.printVec();
    // std::cout << cvdb.printStr() << std::endl;


    // cvdb.resetNum('a');
    // cvdb.convert();
    // cvdb.printVec();
    // std::cout << cvdb.printStr() << std::endl;

    // test for MapDS
    auto mapDS = new MapDS(new ConvertDecBni(0));

    mapDS->MapDS_init();
    std::cout << mapDS->toString('a') << std::endl;
    std::cout << mapDS->toChar("1100001") << std::endl;


    std::cout << mapDS->toString('!') << std::endl;

    if (mapDS) delete mapDS;
    return 0;
}