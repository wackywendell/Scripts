from primes import Primes
import itertools

print("Loading primes...")
ps = Primes()
print(len(ps), "primes loaded.")

class Pattern(object):
    def __init__(self, args):
        def makeint(n):
            try:
                n = int(n)
            except ValueError:
                return -1
            if n < 0:
                return -1
            if n > 9:
                return -1
            return n
        self.pats = list(reversed([makeint(arg) for arg in args]))
    
    def __str__(self):
        mys = ""
        for i in self.pats:
            if i < 0 or i > 10:
                i = "*"
            else:
                i = str(i)
            mys = i + mys
        return mys
    
    def fill(self, val):
        curn = 0
        for (i, n) in enumerate(self.pats):
            if n < 0:
                n = val
            curn += n * (10**i)
        return curn
    
    def getprimes(self, isprime):
        if -1 not in self.pats:
            if isprime(self.fill(0)):
                return [self]
            else:
                return []
        digits = range(10)
        if self.pats[-1] == -1:
            digits = range(1,10)
        return [num for num in digits if isprime(self.fill(num))]
    
    def numprimes(self, isprime):
        return len(self.getprimes(isprime))

def allcombos(ndigits,fdigit=1):
    firstdig = range(fdigit,11)
    middigs = [range(0,11)] * (ndigits-2)
    lastdig = [1,3,7,9]
    digits = [firstdig] + middigs + [lastdig]
    return itertools.product(*digits)
    
    #~ def joiner(arg):
        #~ first, mid, last = arg
        #~ return (first,) + mid + (last,)
    #~ return map(joiner,
        #~ itertools.product(firstdig, middigs, lastdig)
        #~ )

def findn(startdigs, fdigit=1, numps=8, nshow=2):
    found = []
    lastp = ps.getlast()
    print("Loaded primes, last", lastp)
    while not found:
        firstdig = -1
        try:
            for combo in allcombos(startdigs, fdigit):
                if all(d < 10 for d in combo):
                    continue
                p = Pattern(combo)
                if combo[nshow] != firstdig:
                    firstdig = combo[nshow]
                    print("Testing", p, "Last Prime:", ps.getlast(), 
                        "Total primes:", len(ps))
                    #~ if ps.getlast() != lastp:
                        #~ ps.write()
                #~ print("testing",p)
                nprimes = p.numprimes(ps.isprime)
                if nprimes >= numps:
                    found.append(p)
                    print("FOUND!!!", p)
                    
            startdigs += 1
        except KeyboardInterrupt:
            return found
    return found

found = [n for n in findn(6,1,8,1)]
#~ found.sort()
for n in found:
    print(str(n), n.getprimes(ps.isprime), n.fill(n.getprimes(ps.isprime)[0]))
#~ print("Found:")
#~ print(*foundps, sep=", ")

#~ print(list(allcombos(2)))


#~ p = Pattern("56**3")
#~ print(p.numprimes(myps))

#~ exit()
