#!/usr/bin/python

def allgroups(n, lst, start=[]):
    #~ print " "*ind+str(n), lst, start, ind
    ln = len(lst)
    if n <= 0 or n > ln:
        #~ print " "*ind+"DONE"
        return
    if n == ln:
        #~ print " "*ind, "a2:", start + lst
        #~ print " "*ind+"DONE"
        yield start+lst
        return
    if n == 1:
        for i in lst:
            #~ print " "*ind, "b:", start + [i]
            yield start + [i]
        #~ print " "*ind+"DONE"
        return
    i = lst[0]
    lst = list(lst)[1:]
    for j in allgroups(n-1, lst, start+[i]):
        #~ print " "*ind, "c:", j
        yield j
    for j in allgroups(n, lst, start):
        #~ print " "*ind, "d:", j
        yield j
    #~ print " "*ind+"DONE"

def splits(n, lst, start=[], rest=[]):
    ln = len(lst)
    if n > ln:
        return
    elif n == 0:
        yield (start, rest + lst)
        return
    elif n == ln:
        yield (start + lst, rest)
        return
    i = lst[0]
    lst = list(lst)[1:]
    for j in splits(n-1, lst, start+[i], rest):
        #~ print " "*ind, "c:", j
        yield j
    for j in splits(n, lst, start, rest + [i]):
        #~ print " "*ind, "d:", j
        yield j
    #~ print " "*ind+"DONE"

def groupings(groupsize, lst):
    if groupsize >= len(lst):
        yield [lst]
        return
    i = lst[0]
    lst = lst[1:]
    for firstgrp, rest in splits(groupsize - 1, lst, [i]):
        #~ print "firstgrp:", firstgrp
        for othergrps in groupings(groupsize, rest):
            yield [firstgrp] + othergrps
