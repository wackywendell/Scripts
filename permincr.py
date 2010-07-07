from __future__ import (absolute_import, print_function, division, 
                        unicode_literals)
from future_builtins import filter, map, zip
#1234 -> 1243    4321 - 3421
#1243 -> 124 3 -> 142 3 -> 1423
#3421 -> 3 421 -> 3 241 -> 3241

# 4231 -> 423 1 -> 4

def incrold(n):
    digits = [s for s in str(n)]
    rev = list(reversed(digits))
    newlist = []
    
    def combine(newlist, revlist):
        newlist = list(reversed(sorted(newlist)))
        #print("new: {0} - old: {1}".format("".join(newlist), "".join(revlist)))
        return "".join(reversed(newlist + revlist))
        
    while len(rev) >= 2:
        if rev[0] > rev[1]:
            (rev[1], rev[0]) = (rev[0], rev[1])
            newlist.append(rev[0])
            rev = rev[1:]
            return combine(newlist, rev)
        else:
            newlist.append(rev[0])
            rev = rev[1:]
    
    return "".join(digits + ['0'])
    
def incr(n):
    digits = [s for s in str(n)]
    
    loc=-2
    while loc > -len(digits):
        print(loc)
        if digits[loc] < digits[loc+1]:
            firstdig = digits[loc]
            lastbits = digits[loc+1:]
            print(firstdig, lastbits)
            newfirstdig = firstdig
            lastbits.sort()
            for dig in sorted(lastbits):
                if dig > firstdig:
                    newfirstdig = dig
            lastbits.remove(dig)
            lastbits.append(firstdig)
            lastbits.sort()
            return "".join(digits[:loc] + [newfirstdig] + lastbits)
        loc -= 1
    return "".join(digits + ['0'])

import itertools
def tester(lst):
    perms = itertools.permutations(sorted(lst))
    for p in perms:
        p = "".join(p)
        print("{0} -> {1}".format(p, incr(p)))

def incrfile(fname):
    with open(fname) as f:
        givennum = int(f.readline().strip())
        n = 0
        for line in f:
            n += 1
            line = line.strip()
            yield n, line, incr(line)
        if givennum != n:
            msg = """Number at beginning of file wrong size
            Given: {0}; processed: {1}""".format(givennum, n)
            raise IOError, msg

def writefile(finname, foutname):
    with open(foutname, 'w') as f:
        for n, line, incl in incrfile(finname):
            foutline = "Case #{0}: {1}\n".format(n,incl)
            if n % 1000 == 0:
                print(foutline.strip())
            f.write(foutline)

def printoutfile(finname):
    for n, line, incl in incrfile(finname):
        poutline = "{0}\tCase #{1}: {2}".format(line,n,incl)
        foutline = "Case #{0}: {1}".format(n,incl)
        print(poutline)