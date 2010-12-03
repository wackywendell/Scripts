from collections import defaultdict
from itertools import combinations, chain

def subsets(iterable, maxlen = None):
    s = list(iterable)
    if maxlen = None:
        maxlen = len(s)
    return chain.from_iterable(combinations(s, r) for r in range(1,maxlen+1))

def checkopt(s):
    d = defaultdict(set) # dictionary of subsetlen : set(lengths of subsets of this len)
    for sub in subsets(s):
        subsum = sum(sub)
        sublen = len(sub)
        sublens = d[sublen]
        if subsum in sublens:
            return False
        sublens.add(subsum)
    
    lens = sorted(d.keys())
    
    allsublens = set((0,))
    for length in lens:
        cursublens = d[length]
        curmax = max(allsublens)
        for sublen in cursublens:
            if sublen < curmax:
                return False
        allsublens = allsublens.union(cursublens)
    return True

def findnextopt(s,limval = 3):
    curopt = None
    newlen = len(s)+1
    startnum = sorted(s)[newlen//2 - 1]
    print(newlen, startnum)
    possibsets = combinations(range(startnum, startnum + limval*newlen), newlen)
    possibsets = sorted(possibsets, key=sum)
    for curs in possibsets:
        curs = set(curs)
        if not checkopt(curs):
            # current set is not optimal
            continue
        if curopt and sum(curopt) < sum(curs):
            # we already have a better optimal set
            continue
        curopt = curs
        return curs
    
    return curopt

for s in ([4,5,6], [2,4,5,6]):
    print(s, checkopt(s))

optsets = [{1}]
for i in range(4):
    curs = optsets[-1]
    news = findnextopt(curs)
    print(news)
    optsets.append(news)