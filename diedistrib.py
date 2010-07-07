from __future__ import (absolute_import, print_function, division, 
                        unicode_literals)
from future_builtins import filter, map, zip
import itertools

class Memoize:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
    Will only work on functions with non-mutable arguments
    """
    # taken from ActiveState
    def __init__(self, fn):
        self.__doc__ = fn.__doc__
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if not self.memo.has_key(args):
            self.memo[args] = self.fn(*args)
        return self.memo[args]
        

@Memoize
def diedistrib(n):
    """Gives the probability distribution of a roll of n dice
    """
    if n < 1:
        raise ValueError, "n must be greater than 0 and an integer"
    if n == 1:
        return dict([(x,1) for x in range(1,7)])
        
    lowerdict = diedistrib(n-1)
    resdict = {}
    for k,v in lowerdict.items():
        for newroll in range(1,7):
            resdict[k+newroll] = resdict.get(k+newroll,0) + v
    return resdict
        
    # oldway
    if False:
        d = [1,2,3,4,5,6]
        ds = [d] * n
        resdict = {}
        for roll in itertools.product(*ds):
            res = sum(roll)
            resdict[res] = resdict.get(res, 0) + 1
        self.dict[n] = resdict
        return resdict

def matchoff(m, n):
    """Given a stack of m dice and a stack of n dice, returns the number of times
    the first stack will (win, tie, lose) to the second stack, as a tuple
    """
    rollsa = diedistrib(m)
    rollsb = diedistrib(n)    
    wins = losses = ties = 0
    for rolla in rollsa:
        for rollb in rollsb:
            times = rollsa[rolla] * rollsb[rollb]
            if rolla > rollb:
                wins += times
            elif rollb > rolla:
                losses += times
            else:
                ties += times
    return (wins, ties, losses)
diedistrib.matchoff = matchoff
del matchoff

def chancetobeat(m,n):
    """returns the chance a stack of m dice will beat a stack of n dice"""
    wins, ties, loss = diedistrib.matchoff(m,n)
    return wins / (wins + ties + loss)

diedistrib.chancetobeat = chancetobeat
del chancetobeat
