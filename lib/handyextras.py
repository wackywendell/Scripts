from __future__ import (absolute_import, print_function, division, 
                        unicode_literals)
from future_builtins import filter, map, zip

import __builtin__
from functools import wraps
from contextlib import contextmanager
import sys

def showbs(obj, indent = ''):
    if not isinstance(obj, type):
        if hasattr(obj, '__class__'):
            obj = obj.__class__
        else:
            obj = type(obj)
    print(indent + repr(obj))
    if not hasattr(obj, '__bases__'):
        return
    for b in obj.__bases__:
        if obj != b:
            showbs(b, indent + '  ')

if False:
    def showbs(obj):
        if not isinstance(obj, type):
            if hasattr(obj, '__class__'):
                obj = obj.__class__
            else:
                obj = type(obj)
        if not hasattr(obj, '__bases__') or not obj.__bases__:
            return obj
        bases = tuple(showbs(b) for b in obj.__bases__)
        if len(bases) == 1:
            bases = bases[0]
        return obj, bases

    

def uprint(*args, **kwargs):
    newargs = [unicode(x) for x in args]
    return __builtin__.print(*newargs, **kwargs)

@contextmanager
def replacestdouterr(fname, mode='aw'):
    normerr, normout = sys.stderr, sys.stdout
    with open(fname, mode) as f:
        sys.stderr = sys.stdout = f
        yield
        sys.stderr, sys.stdout = normerr, normout


def printstofile(fname, mode='aw'):
    def printsdeco(func):
        @wraps(func)
        def newfunc(*args, **kwargs):
            with replacestdouterr(fname, mode):
                return func(*args, **kwargs)
        return newfunc
    return printsdeco


def printkws(func):
    @wraps(func)
    def g(*args, **kwargs):
        argstrs = [repr(arg) for arg in args]
        kwstrs = ["{0}={1!r}".format(k,v) for k,v in kwargs.items()]
        allargs = ", ".join(argstrs + kwstrs)
        strcall = str(func.func_name) + '(' + allargs + ')'
        print('Entering', strcall)
        retval = func(*args, **kwargs)
        print(strcall, '=', repr(retval))
        return retval
    return g

def tmplog(func):
    return printstofile('/tmp/py.log')(printkws(func))
    
__all__ = ['showbs', 'printstofile', 'printkws', 'tmplog']
