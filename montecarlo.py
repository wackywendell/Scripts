"""
Monte Carlo simulation!
"""
from __future__ import (absolute_import, print_function, division, 
                        unicode_literals)
from future_builtins import filter, map, zip
from numpy import array, ndarray
import numpy as np

class shamiltonian(ndarray):
    def __new__(cls, *args):
        buf = args
        if not args:
            buf = None
        obj = ndarray.__new__(cls, shape=(1, 4), dtype=int, buffer=buf)
        return obj
    def apply(self, slist):
        "not yet written"
        pass

class hamiltonian(ndarray):
    def __new__(cls, *args):
        obj = ndarray.__new__(cls, shape=(2**len(args), 2**len(args)),
                dtype=int)
        obj.termnums = array(args)
        return obj

class statelist(list):
    def __init__(self, lst=()):
        for obj in lst:
            self.typecheck(obj)
        list.__init__(self, lst)
    def __setitem__(self, *args):
        print("setitem",args,sep="")
        return list.__setitem__(self, *args)
    def __setslice__(self, start, end, sobj):
        print("setslice",(start,end,sobj),sep="")
        for obj in sobj:
            self.typecheck(obj)
        return list.__setslice__(self, start, end, sobj)
    def append(self, obj):
        self.typecheck(obj)
        list.append(self, obj)
    def prepend(self, obj):
        self.typecheck(obj)
        list.prepend(self, obj)
        
    def typecheck(self, obj, err=True):
        if obj is not 0 and obj is not 1:
            if err:
                raise TypeError, "statelist can only take values 0 and 1; given value " + repr(obj)
            else:
                return False
        return True
    
    def ustr(self):
        print("ustr called!")
        def conv(obj):
            return u'\u2191' if obj == 0 else u'\u2193'
        obj = u"".join(conv(obj) for obj in self)
        #print(obj)
        return obj
