import itertools
import sys
version = sys.version
"""
An updated version of my diedistrib module, implemented as a class with memoizing, and compatible with Shedskin 3.1
"""

import string

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
