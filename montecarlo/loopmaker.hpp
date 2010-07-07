#include "basicobjs.hpp"

/* This defines the basic classes for the module.
 * 
 * hamiltpair:
 *   represents a hamiltonian acting on two (of many) qbits.
 *   includes data on which two qubits, as well as methods to
 *   apply itself to two qubits
 * statelist:
 *   just a vector of 0s and 1s.
 *   can also apply a hamiltonian to itself
 * loopmaker:
 *   generates the first setup, and then later 
 * 
 */



// A base class for generating a loop.
// This base doesn't generate any loop, but sets up the basis for it;
// we can derive from it in order to get different functionality
class loopmaker{
    protected:
        vector<uint> qbitvec;
        vector<uint> hamiltnumvec;
        hamilstates myhamilstates;
        
    public:
        loopmaker();
        virtual ~loopmaker();
        
        // check that the steps only go up or down,
        // left or right by one step
        // does not fix errors
        bool checkintegrity();
        // check that its gone full circle (includes integrity check)
        bool checkcircularity();
        
        // This is the method that should be 
        // overridden for new functionality
        // the base version just chooses random directions with no
        // bias
        virtual void generateloop() = 0; // PURE VIRTUAL
        
        float randfloat();
        void randperm(vec);
};

class randloopmaker : loopmaker{
    private:
        uint numqbits;
        uint numhamils;
    public:
        randloopmaker(uint qbits, uint hamils);
        ~randloopmaker();
    
        void generateloop();
};
    