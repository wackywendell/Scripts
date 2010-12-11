import math
from fpath import *
from itertools import takewhile

pfile = File("~/scripts/pychall/primes.txt").norm()

class Primes(object):
    plst = [2]
    pset = set([2])
    curp = 3
    
    def __init__(self, usefile=None):
        self.usefile = File(usefile)
    
    def calcnext(self):
        primestotest = takewhile(lambda x: x <= math.sqrt(self.curp),
                                                self.plst)
        if any(self.curp % p == 0 for p in primestotest):
            self.curp += 2
            return
        else:
            self.plst.append(self.curp)
            self.pset.add(self.curp)
            self.curp += 2
            return self.curp - 2
    
    def __enter__(self):
        self.read()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.write()
    
    def calcto(self, n):
        while self.curp <= n:
            self.calcnext()
    
    def calcn(self, n):
        while len(self.plst) < n:
            self.calcnext()
            
    def __iter__(self):
        return iter(self.plst)
    
    def __len__(self):
        return len(self.plst)
    
    def write(self):
        txt = '\n'.join((str(n) for n in self))
        with  self.usefile.open('w') as f:
                f.write(txt)
                print("Wrote file.")
    
    def read(self):
        if not self.usefile.exists():
            return
        with self.usefile.open('r') as f:
            txt = f.read()
        for l in txt.split('\n'):
            l = l.strip()
            if l:
                self.pset.add(int(l))
        
        self.plst = sorted(self.pset)
        newcurp = ((self.plst[-1] + 2) // 2) * 2 + 1
        self.curp = max(self.curp, newcurp)
    
    def isprime(self, n):
        self.calcto(n)
        return n in self.pset
    
    def __del__(self):
        try:
            if self.usefile:
                self.write()
        except Exception as e:
            print(e)
    
    def getlast(self):
        return self.plst[-1]

if __name__ == "__main__":
    print("Loading primes...")
    with Primes(pfile) as p:
        print("Primes loaded.")
        stp = 1000
        for i in range(stp*(p.getlast() // stp), 20*1000+1, stp):
            print(i)
            if p.isprime(i+3):
                print("Prime:", i)
            print("len:", len(p),"last:", p.getlast(), "current:", p.curp)
        #~ p.write()
        print(len(p), p.getlast(), p.curp)
    #~ del p
    exit()
