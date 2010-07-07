from __future__ import (absolute_import, print_function, division, 
                        unicode_literals)
from future_builtins import filter, map, zip
import __builtin__

def showbs(obj, indent = ''):
    if not isinstance(obj, type):
        obj = obj.__class__
    print(indent + repr(obj))
    for b in obj.__bases__:
        if obj != b:
            showbs(b, indent + '  ')

def uprint(*args, **kwargs):
    newargs = [unicode(x) for x in args]
    return __builtin__.print(*newargs, **kwargs)
