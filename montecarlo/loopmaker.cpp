#include "loopmaker.hpp"

loopmaker::loopmaker(){
        srand( (unsigned)time( NULL ) );
};

loopmaker::~loopmaker(){};

//void loopmaker::generateloop(){
    //cout << "THIS METHOD DOESN'T EXIST!" << endl;
//}

bool loopmaker::checkintegrity(){
    uint sz = qbitvec.size();
    if(hamiltnumvec.size() != sz) return false;
    
    uint leftright = 0;
    uint updown = 0;
    for(uint i = 1; i < sz; i++){
        leftright = abs(int((qbitvec[i]) - (qbitvec[i-1])));
        if(leftright == sz-1) leftright = 1; // allow travel around edges
        updown = abs(int(hamiltnumvec[i] - hamiltnumvec[i-1]));
        if(updown == sz-1) updown = 1; // allow travel around edges
        // every step should be a distance of 1 from the previous
        if(updown + leftright != 1) return false;
    }
    return true;
}

bool loopmaker::checkcircularity(){
    int sz = qbitvec.size();
    if(qbitvec[sz-1] == qbitvec[0] && 
       hamiltnumvec[sz-1] == hamiltnumvec[0]) return true;
    return false;
}

float loopmaker::randfloat(){
    // generates a random float between 0 and 1.
    // TODO:
    // This needs a better generator. Maybe use a BOOST library?
    
    return (float) rand()/RAND_MAX;
}

void loopmaker::randperm(vec v){
    // simple algorithm taken from
    // http://rgrig.blogspot.com/2005/04/random-permutation.html
    // modified heavily to fit this spot
    // I'm sure its a fairly standard algorithm, I just didn't know it
    // recursively randomizes the order as it goes along
    // as it gets to step i; it switches v[i] with v[newloc], where newloc
    // is a random int, representing a random spot in the previously
    // randomly sorted vector
    
    int tmp;
    int newloc;
    for(uint i=0; i<v.size(); i++){
        tmp = v[i];
        newloc = randfloat() * i;
        v[i] = v[newloc];
        v[newloc] = tmp;
    }
}

randloopmaker::randloopmaker(uint qn, uint hn){
    myhamilstates.statesvec.resize(hn);
    myhamilstates.hamiltvec.resize(hn);
    for(uint i=0; i<hn; i++){
        myhamilstates.statesvec[0].resize(qn);
    }
    // set the first row of qbits to random
    for(uint i=0; i<qn; i++){
        myhamilstates.statesvec[0][i] = int(randfloat() + .5);
    }
    
    // our generic hamiltonian
    hamiltpair generichamil = hamiltpair();
    for(uint i=0; i<generichamil.size(); i++){
        generichamil[i] = i;
        generichamil.lqbitn=0;
        generichamil.rqbitn=1;
    }
    
    // put the hamiltonians in random places
    for(uint i=0; i<hn; i++){
        
    }
};
randloopmaker::~randloopmaker(){};

void randloopmaker::generateloop(){
    qbitvec.resize(0);
    hamiltnumvec.resize(0);
}
