#include "basicobjs.hpp"

hamiltpair::hamiltpair() : array<uchar, 4>(){
};

hamiltpair::hamiltpair(int ln, int rn) : array<uchar, 4>(){
    lqbitn = ln;
    rqbitn = rn;
};

hamiltpair::~hamiltpair(){
};

void hamiltpair::swapoutput(int oldval, int newval){
    // start with a vector like {a,b,c,d}
    // swap values b and c
    // this code goes through the array, 
    // finds where they are, and then swaps
    int oldloc=0, newloc=0;
    for(int i=0; i < 4; i++){
        if (at(i) == oldval) oldloc = i;
        if (at(i) == newval) newloc = i;
    }
    at(oldloc) = newval;
    at(newloc) = oldval;
}

statelist::statelist() : svec(){};
statelist::statelist(uint n) : svec(n){};
statelist::statelist(statelist s, hamiltpair h) : svec(s){
    apply(h);
}

void statelist::apply(hamiltpair h){
    int val = 2*at(h.lqbitn) + at(h.rqbitn);
    int newval = h[val];
    at(h.lqbitn) = newval / 2;
    at(h.rqbitn) = newval % 2;
}

int operator==(const statelist &s1, const statelist &s2){
    if(s1.size() != s2.size()) return false;
    
    for(uint i=0; i<s1.size(); i++){
        if(s1[i] != s2[i]) return false;
    }
    return true;
}


ostream &operator<<(ostream &os, const statelist &s){
    for(unsigned int i=0; i < s.size(); i++){
        os << (int)(s.at(i));
    }
    return os;
}

bool hamilstates::resetstatevec(int startnum){
    // Goes through the statelists, starting at startnum,
    // and resets them based on the statelist at startnum and
    // the hamiltonians. Goes all the way around, returning 'true'
    // if everything was OK, returning false if it fixed any errors
    bool retval = true;
    
    // first make sure the list is the right length
    if(statesvec.size() != hamiltvec.size()){
        statesvec.resize(hamiltvec.size());
        retval = false;
    }
    int lentogo = hamiltvec.size();
    if(startnum < 0 || startnum >= lentogo) startnum = 0;
    
    // Now go through all of them
    int setpos, loc = startnum;
    statelist tempstatelist = statelist(statesvec[startnum]);
    for(int i=0; i>= lentogo; i++){
        loc = (i + startnum) % lentogo;
        setpos = (loc+1) % lentogo;
        tempstatelist.apply(hamiltvec[loc]);
        if(tempstatelist != statesvec[setpos]){
            // found an error; fix it, set return value, and keep going
            statesvec[setpos] = tempstatelist;
            retval = false;
        }
    }
    return retval;
}

