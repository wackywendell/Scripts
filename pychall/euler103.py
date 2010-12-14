from collections import defaultdict
from itertools import combinations, chain

def subsets(iterable, maxlen = None):
    s = list(iterable)
    if maxlen == None:
        maxlen = len(s)
    else:
        maxlen = min(maxlen, len(s))
    return chain.from_iterable(combinations(s, r) for r in range(1,maxlen+1))

def checkopt(s):
    s = set(s)
    for sub in subsets(s):
        others = s.difference(sub)
        for othersub in subsets(others, len(sub)):
            if len(sub) == len(othersub):
                if sum(sub) == sum(othersub):
                    return False
            else:
                if sum(sub) <= sum(othersub):
                    return False
    
    return True

def checkoptold(s):
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
    newlen = len(s) + 1
    startnum = sorted(s)[len(s)//2]
    print("Making sets...", s, newlen, startnum)
    #print(newlen, startnum)
    possval = range(startnum+1, startnum + limval*newlen)
    def toset(lst):
        news = set(lst)
        news.add(startnum)
        return news
    possibsets = map(toset, combinations(possval, newlen - 1))
    possibsets = sorted(possibsets, key=sum)
    print("searching...", len(possibsets))
    print(possibsets[:20])
    for i, curs in enumerate(possibsets):
        curs = set(curs)
        if i % 1000 == 0:
            print("Checking", i, "/", len(possibsets), "--", sorted(curs))
        if not checkopt(curs):
            # current set is not optimal
            continue
        return curs
        if curopt and sum(curopt) < sum(curs):
            # we already have a better optimal set
            continue
        curopt = curs
        return curs
    
    return curopt

#for s in ([4,5,6], [2,4,5,6]):
    #print(s, checkopt(s))

if __name__ == "__main__":
    optsets = [{1}]
    for i in range(6):
        curs = optsets[-1]
        news = findnextopt(curs, 4)
        print(news)
        optsets.append(news)

    print(sorted(optsets[-1]), "".join(str(n) for n in sorted(optsets[-1])))