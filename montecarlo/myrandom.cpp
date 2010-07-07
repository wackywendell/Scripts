#include "myrandom.hpp"

bool myrandom::initialize(){
    // we only want to seed once, and initialized tells us if we've seeded
    static bool initialized=false;
    if (initialized) return false; // return value is whether we initialized
    
    srand(time(0));
    
    // now that we've seeded, we set the initialized value to 'true' and return
    initialized=true;
    return true;
    
}

uint myrandom::randint(uint max){
    myrandom::initialize();
    return rand() % max;
}

float myrandom::randfloat(){
    // generates a random float between 0 and 1.
    // TODO:
    // This needs a better generator. Maybe use a BOOST library?
    myrandom::initialize();
    
    return (float) rand()/RAND_MAX;
}

void myrandom::randperm(vec v){
    // simple algorithm taken from
    // http://rgrig.blogspot.com/2005/04/random-permutation.html
    // modified heavily to fit this spot
    // I'm sure its a fairly standard algorithm, I just didn't know it
    // recursively randomizes the order as it goes along
    // as it gets to step i; it switches v[i] with v[newloc], where newloc
    // is a random int, representing a random spot in the previously
    // randomly sorted vector
    myrandom::initialize();
    
    int tmp;
    int newloc;
    for(uint i=0; i<v.size(); i++){
        tmp = v[i];
        newloc = randfloat() * i;
        v[i] = v[newloc];
        v[newloc] = tmp;
    }
}