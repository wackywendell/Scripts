import itertools
import sys
import numpy as np
import collections
version = sys.version
"""
An updated version of my diestacks module, implemented as a class with memoizing
"""

class Diestack(object):
    _memo = {}
    
    def __new__(cls, obj):
        if isinstance(obj, cls):
            return obj
        elif isinstance(obj, np.ndarray):
            return cls._makefromarr(obj)
        
        n = int(obj)
        if 1 not in cls._memo:
            arr = np.array([1] * 6, dtype=np.uint64, copy=False)
            cls._makefromarr(arr)
        
        return cls._getn(n)
    
    @classmethod
    def _makefromarr(cls, arr):
        obj = object.__new__(cls)
        obj.arr = np.array(arr, dtype=np.uint64, copy=False)
        n = cls._findndice(obj.arr)
        if n not in cls._memo:
            cls._memo[n] = obj
        return obj
    
    @classmethod
    def _getn(cls, n):
        mdict = cls._memo
        
        curn = n
        curobj = 1
        
        keys = mdict.keys()
        
        while curn > 0:
            keys = [k for k in mdict.keys() if k <= curn]
            curk = max(keys)
            #print keys, curk, curn
            curobj *= mdict[curk]
            #print curobj
            curn -= curk
        
        return curobj
    
    @classmethod
    def _resetmemo(cls):
        for k in cls._memo.keys():
            if k > 1:
                del cls._memo[k]
    
    @classmethod
    def _listk(cls):
        return list(cls._memo.keys())
    
    def __init__(self, obj):
        pass
    
    @property
    def ndice(self):
        return self._findndice(self.arr)
    
    @staticmethod
    def _findndice(obj):
        # 1-6  : 6
        # 2-12 : 11
        # 3-18 : 16
        return (len(obj) - 1) // 5
    
    @staticmethod
    def _getarrlen(n):
        return 5 * n + 1
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __mul__(self, other):
        if other == 1:
            return self
        arr1 = np.array(self.arr, copy=False, dtype=np.uint64)
        if isinstance(other, Diestack):
            arr2 = np.array(other.arr, copy=False, dtype=np.uint64)
        else:
            arr2 = np.array(other, copy=False, dtype=np.uint64)
        if len(arr2) > len(arr1):
            arr1, arr2 = arr2, arr1
        
        wdth = len(arr1) + len(arr2) - 1
        lngth = len(arr2)
        bigarr = np.zeros((lngth, wdth),dtype=np.uint64)
        for n, val in enumerate(arr2):
            wdth = len(arr1)
            #print "wdth", wdth
            #print "bigarr:", bigarr
            #print "bigarr:",len(bigarr[n,n:(n+wdth)])
            #print "arr1:",len(arr1)
            bigarr[n,n:(n+len(arr1))] = val * arr1
        return self.__class__(bigarr.sum(0))
    
    def __str__(self):
        return str(self.arr)
    def __repr__(self):
        return ("Diestack(" + str(self.ndice) + "):"
                + str(self.arr))
                
    def __pow__(self, n):
        newd = 1
        for i in range(int(n)):
            newd *= self
        return newd
        
    def __len__(self):
        return len(self.arr)
    def __iter__(self):
        return iter(self.arr)
    
    def matchoff(self, other):
        other = self.__class__(other)
        wins = losses = ties = 0
        for la, rolla in enumerate(self):
            vala = la + self.ndice
            for lb, rollb in enumerate(other):
                valb = lb + other.ndice
                times = rolla * rollb
                if rolla > rollb:
                    wins += times
                elif rollb > rolla:
                    losses += times
                else:
                    ties += times
        return (wins, ties, losses)
        
d=Diestack

class Diestacks:
    def __init__(self):
        mindict = dict([(x,1) for x in xrange(1,7)])
        self.memo = {1:mindict}
    
    def diedistrib(self, n):
        """Gives the probability distribution of a roll of n dice
        """
        if n in self.memo:
            return self.memo[n]
        if n < 1:
            raise ValueError("n must be greater than 0 and an integer")
        
        while max(self.memo.keys()) < n:
            curmax = max(self.memo.keys())
            lowerdict = self.memo[curmax]
            resdict = {1:1} # fancy footwork to get the type to work out
            del resdict[1]
            for k,v in lowerdict.items():
                for newroll in xrange(1,7):
                    resdict[k+newroll] = resdict.get(k+newroll,0) + v
            self.memo[curmax+1] = resdict
            #
        return self.memo[n]

    def matchoff(self, m, n):
        """Given a stack of m dice and a stack of n dice, returns the number of 
        times the first stack will (win, tie, lose) to the second stack, as a 
        tuple
        """
        rollsa = self.diedistrib(m)
        rollsb = self.diedistrib(n)    
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

    def chancetobeat(self, m,n):
        """returns the chance a stack of m dice will beat a stack of n dice"""
        wins, ties, loss = self.matchoff(m,n)
        return wins / float(wins + ties + loss)
    
    def risk(self, m,n):
        w,t,l = self.matchoff(m,n)
        total=w+t+l
        return n*w/total - (m-1)*(t+l)/total
    
    def pdistrib(self, n):
        dct = self.diedistrib(n)
        mx = max(dct.values())
        
        magicnum = 80-5-1-len(str(mx))
        
        if mx < magicnum:
            mx = magicnum
        
        for k in sorted(dct.keys()):
            n = dct[k]
            m = n *magicnum//mx
            #print("{0:3d}: {1} {2}".format(k, m*"=", n))
            print "%3d: %s, %d" % (k, m*'=', n)
    
    #def plotdistrib(self, n):
        #import pylab
        #dct = self.diedistrib(n)
        #pairs = dct.items()
        #(x,y) = zip(*pairs)
        #pylab.plot(x,y)
        

die = Diestacks()

if __name__ == '__main__':
    if False: # stuff for Shedskin
        die.diedistrib(8)
        die.pdistrib(8)
        die.chancetobeat(8,8)
        die.matchoff(8,8)
