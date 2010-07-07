#include <iostream>
#include <vector>
using namespace std;
#include "loopmaker.hpp"
#include "myrandom.hpp"

//typedef vector<int> vec;
//typedef vector<vector<int> > matr;

int main( int argc, const char* argv[] ){
    cout << "--- MAIN ---" << endl;
    statelist s = statelist(3);
    s[0] = s[1] = s[2] = 0;
    
    cout << s << endl;
    cout << RAND_MAX << endl;
};