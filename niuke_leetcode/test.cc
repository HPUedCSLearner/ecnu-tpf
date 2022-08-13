#include <stdio.h>
#include <string.h>

#include <climits>
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <queue>
#include <utility>
#include <map>

using namespace std;

class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.length(), n = word2.length();
        word1 = ' ' + word1;   word2 = ' ' + word2;
        vector<vector<int> > f(m + 1, vector<int>(n + 1, INT_MAX));

        for (int i = 0; i <= n; ++i) f[0][i] = i;
        for (int j = 0; j <= m; ++j) f[j][0] = j;

        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                // cout << "(" << i << " , " << j << ")" << endl;
                if (word1[i] == word2[j]) {
                    f[i][j] = f[i-1][j-1];
                } else {
                    f[i][j] = min(f[i][j-1], min(f[i-1][j], f[i-1][j-1])) + 1;
                }
            }
        }
        
        return f[m][n];
    }
};

void test() {
    vector<int> vecA = {3, 4, 5, 6, 7, 8, 9};
    for (auto item : vecA) {
        cout << item << "-";
    } cout << endl;

    int a[] = {3, 4, 5, 6, 7, 8, 9};
    cout << "sizeof (a) " << sizeof(a) / sizeof(a[0]) << endl;

    memset(a, 0, sizeof(a));
    vector<int> vecB(a, a + sizeof(a));
    cout << "vetB.size()" << vecB.size() << endl;
    for (auto item : vecB) {
        cout << item << "-";
    } cout << endl;

    std::vector<double> values(3, 3.1415926);
    for (auto item : values) {
        cout << item << "-";
    } cout << endl;

    vector<int> vecC(std::begin(a), std::end(a));
    for (auto item : vecC) {
        cout << item << "-";
    } cout << endl;


    cout << end(a) - begin(a) << endl;

    fill(begin(a), end(a), 100);
    vector<int> vecD(std::begin(a), prev(std::end(a), 1));
    for (auto item : vecD) {
        cout << item << "-";
    } cout << endl;

    vector<int> vecE(3, 99);
    vector<vector<int>> arr(3, vector<int>(3, 99));
    for (auto vec : arr) {
        for (auto item : vec) {
            cout << item << " ";
        } cout << endl;
    }
    
}

void test2() {
    
    vector<int>values{1,2,3};
    cout << "values 容器首个元素的地址：" << values.data() << endl;
    auto first = values.begin();
    auto end = values.end();

    for (auto item : values) {
        cout << item << "-";
    } cout << endl;

    //增加 values 的容量
    values.reserve(20);
    cout << "values 容器首个元素的地址：" << values.data() << endl;
    while (first != end) {
        cout << *first;
        ++first;
    }

    for (auto item : values) {
        cout << item << "-";
    } cout << endl;


}

void test3() {
    set<string> myset;
    cout << "1、myset size = " << myset.size() << endl;
    myset.insert("http://c.biancheng.net/java/");
    myset.insert("http://c.biancheng.net/stl/");
    myset.insert("http://c.biancheng.net/python/");
    cout << "2、myset size = " << myset.size() << endl;

    //利用双向迭代器，遍历myset
    for (auto iter = myset.begin(); iter != myset.end(); ++iter) {
        cout << *iter << endl;
    }
    cout << "---------------------------" << endl;

    cout << *myset.find("http://c.biancheng.net/java/") << endl;

    myset.erase("http://c.biancheng.net/java/");
    //利用双向迭代器，遍历myset
    for (auto iter = myset.begin(); iter != myset.end(); ++iter) {
        cout << *iter << endl;
    }
    cout << "---------------------------" << endl;

    myset.erase(myset.find("http://c.biancheng.net/java/"));
    //利用双向迭代器，遍历myset
    for (auto iter = myset.begin(); iter != myset.end(); ++iter) {
        cout << *iter << endl;
    }
    cout << "---------------------------" << endl;

}

struct Fruit {
    string name;
    int price;
    friend bool operator<(const Fruit& lhs, const Fruit& rhs) {
        return lhs.price < rhs.price;
    }
};
struct cmp {
    bool operator()(const Fruit& lhs, const Fruit& rhs) {
        return lhs.price > rhs.price;
    }
};

void test4() {
    priority_queue<int> priQue;
    priority_queue<int, vector<int>, less<int>> proQueue;
    priority_queue<Fruit, vector<Fruit>, cmp> que;

    priority_queue<Fruit> fruit;
    fruit.push({"apple", 3});
    fruit.push({"pear", 7});
    fruit.push({"bana", 2});
    fruit.push({"ganzhe", 9});
    cout << fruit.top().name << endl;
    cout << fruit.top().price << endl;

    que.push({"apple", 3});
    que.push({"pear", 7});
    que.push({"bana", 2});
    que.push({"ganzhe", 9});
    cout << que.top().name << endl;
    cout << que.top().price << endl;
    
    pair<string, int> p {"haah", 5};
    cout << p.first << endl;
    cout << p.second << endl;

    map<string, int> str_int;
    str_int.insert({"haha", 100});
    str_int.insert({"xuxu", 300});


}

int main() {
    // test();
    // test2();
    test4();
    return 0;
}