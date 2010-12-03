#from future_builtins import filter, map

from math import sqrt
from itertools import islice, takewhile, chain, repeat, starmap
from collections import Iterable, Container
from orderedset import OrderedSet

class PrimeGen(Iterable, Container):
    _primes = OrderedSet([2])
    _pcur = 3
    
    def __init__(self):
        self.iterpos = 0
    
    def _nextnum(self):
        pcur = self._pcur
        self._pcur += 2
        for x in takewhile(lambda x: x <= sqrt(pcur), self._primes):
            if pcur % x == 0:
                return None
        self._primes.add(pcur)
        return pcur
    
    def __call__(self):
        nextp = None
        while not nextp:
            nextp = self._nextnum()
        return nextp
    
    def __iter__(self):
        return chain(
                iter(self._primes),
                starmap(self, repeat(()))
                )
    
    @property
    def num(self):
        return len(self._primes)
    
    def calcto(self, n):
        "Find all primes up to n"
        while self._pcur <= n:
            self._nextnum()
    
    def calcn(self, n):
        "Find the first n primes"
        while self.num < n:
            self()
    
    def findto(self, n):
        "Return all primes less than n"
        return takewhile(lambda x: x <= n, self)
    
    def findn(self, n):
        "Return the first n primes"
        return islice(self, n)
        
    def isprime(self, num):
        self.calcto(num)
        return num in self._primes
        
    def __contains__(self, n):
        return self.isprime(n)
    
p = PrimeGen()
