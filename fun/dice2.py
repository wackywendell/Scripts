#try to use psyco for a speed boost
try:
    import psyco
    psyco.full()
except ImportError:
    pass

from dice import die, k_subsets, testdice, comparewins
from groups import groupings

# implementation #1 for getting all possible combinations of 3 dice with
# nside sides
# this one is faster. It looks shorter, but only because all the code is in
# the groupings module
def getgdice(nside):
    for dice in groupings(nside, range(1, 1 + 3*nside)):
        yield [die(d) for d in dice]

# implementation #2
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
            
            curlst = [fst, snd, thd]
            yield curlst

# given nsides, what's the best you can do?
# 'best' is defined by the dice.py 'comparewins' function
# as of this comment, 'best' is defined by the minimum of the wins each dice has
# over the one it beats - so if D1 beats D2 by 9, D2 beats D3 by 11, and D3 
# beats D1 by 13, then '9' is its 'rank'
# this gives quite a few 'best' dice combinations
def getbest(nside, curwins=(0,0,0), prt=True):
    curwins = tuple(abs(x) for x in curwins)
    curposs = []
    for (a,b,c) in getgdice(nside):
        wins = testdice(a,b,c)
        if not wins:
            continue
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

def prof(n):
    from cProfile import run
    run('getbest('+str(n)+',prt=False)')
