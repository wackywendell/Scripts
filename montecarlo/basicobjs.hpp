#include <boost/multi_array.hpp>
#include <boost/array.hpp>
using namespace boost;

#include <vector>
using namespace std;

#include <iostream>

typedef unsigned int uint;
typedef unsigned char uchar;
typedef vector<int> vec;
typedef vector<uchar> svec;
typedef multi_array<int,2> matrix;
typedef matrix::index matr_index;


/* A hamiltonian representation for two qbits.
 * Represents only a hamiltonian that takes basis elements to basis elements
 * includes lqbitn and rqbitn, which denote which qubits 
 * are being operated on
 * 
 * if x = hamiltpair[i], then that means state i gets mapped to state x
 */

class hamiltpair: public array<uchar, 4> {
    public:
        hamiltpair();
        hamiltpair(int ln, int rn);
        ~hamiltpair();
        
        uint lqbitn; // l for left (or lower numbered)
        uint rqbitn; // r for right
        
        // swap which two states give oldval, newval when its applied to
        // a state
        void swapoutput(int oldval, int newval);
        
        //TODO:
        //bool checkintegrty(); // makes sure that the hamiltonian is valid
};

// Represents a basis state
// TODO: with a 0 or 1 for each qbit, itcould take up much less memory...
// right now it uses a whole byte for each 0 or 1
class statelist: public svec{
    friend ostream &operator<<(ostream &os, const statelist &s);
    friend int operator==(const statelist &s, const statelist &s2);
    public:
        statelist();
        statelist(uint n);
        statelist(statelist s, hamiltpair h);
        ~statelist(){};
        void apply(hamiltpair);
};

class hamilstates{
    // holds a list of hamiltonians and states
    // the nth state vector is *before* the nth hamiltonian
    // the last state vector doesn't exist; it should be equal
    // to the first
    protected:
    public:
        vector<statelist> statesvec;
        vector<hamiltpair> hamiltvec;
        
        hamilstates(){};
        ~hamilstates(){};
        
        // check that everything is ok, fix errors
        bool resetstatevec(int startnum=0);
};