
#include <stdio.h>
#include <iostream>
#include <stack>
#include <vector>

std::stack<int> st;
std::vector<int> vec;
int do_multi(int a, int b)
{
	return a * b;
}
 
 
int do_calc(int a, int b)
{
	return do_multi(a, b);
}
 
 
int main()
{
	st.push(3);
	vec.push_back(32);
	int a = 4, b = 5;
	printf("result: %d\n", do_calc(a, b));

    for(int i = 0 ;i  < 10; ++i) {
        do_calc(a, b);
    }
	st.pop();
	return 0;
}