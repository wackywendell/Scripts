#!/usr/bin/python

class die(list):
    def test(self):
        print "TEST"
    def cmp(self,other):
        wins=0
        for x in self:
            for y in other:
                if x > y:
                    wins += 1
                #~ elif y > x:
                else:
                    wins -= 1
        return wins
        #~ return sum(cmp(x,y) for x in self for y in other)
    def beats(self, other):
        w = self.cmp(other)
        return w > 0
    def __str__(self):
        return str(list(self))
    def __repr__(self):
        return repr(list(self))

a=die((1,10,11,12,13,14))
b=die((2,3,4,15,16,17))
c=die((5,6,7,8,9,18))

a1=die((2,4,9))
b1=die((1,6,8))
c1=die((3,5,7))

a2=die((18,13,11,9,4,2))
b2=die((17,15,10,8,6,1))
c2=die((16,14,12,7,5,3))

a3=die((18,17,10,9,2,1))
b3=die((16,15,8,7,6,5))
c3=die((14,13,12,11,4,3))

def testdice(a,b,c):
    ab = a.cmp(b)
    bc = b.cmp(c)
    ca = c.cmp(a)
    #~ tot = abs(ab + bc +ca)
    if (ab > 0 and bc > 0 and ca > 0) or (ab < 0 and bc < 0 and ca < 0):
        return (ab, bc, ca)
    else:
        return False

def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    '''
    Yield all subsets of size k from set (or list) s
    s -- a set or list (any iterable will suffice)
    k -- an integer > 0
    '''
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield set(s[i] for i in k_set)

def getdice(nside):
    totnum = range(1,nside*3+1)
    firstdice = k_subsets(totnum, nside)
    possib=[]
    for fstdie in firstdice:
        fst = die(fstdie)
        fst.sort()
        leftovers = set(totnum) - fstdie
        for snddie in k_subsets(leftovers, nside):
            snd = die(snddie)
            snd.sort()
            if fst > snd: continue
            thd = die(set(leftovers) - snddie)
            thd = die(set(leftovers) - snddie)
            thd.sort()
            
            if snd > thd: continue
            
            testresult = testdice(fst, snd, thd)
            if testresult:
                curlst = [fst, snd, thd]
                if curlst not in possib:
                    possib.append(curlst)
                    yield curlst

def comparewins((x1, x2, x3), (y1, y2, y3)):
    xabs = (abs(x1), abs(x2), abs(x3))
    yabs = (abs(y1), abs(y2), abs(y3))
    xm = min(xabs)
    ym = min(yabs)
    xs = sum(xabs)
    ys = sum(yabs)
    if xm > ym:
        return 1
    elif xm < ym:
        return -1
    #~ elif xs > ys:
        #~ return 1
    #~ elif xs < ys:
        #~ return -1
    else: return 0

def getbest(nside, curwins=(0,0,0), prt=True):
    curposs = []
    for (a,b,c) in getdice(nside):
        wins = testdice(a,b,c)
        winsabs = tuple(abs(x) for x in wins)
        compval = comparewins(winsabs, curwins)
        if compval == 1:
            curwins = winsabs
            curposs = [(a,b,c) + winsabs]
            if prt: print ('-' * 50)
            if prt: print (a,b,c) + winsabs
        elif compval == 0:
            curposs.append((a,b,c) + winsabs)
            if prt: print (a,b,c) + winsabs
    return curposs
