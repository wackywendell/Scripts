#!/usr/bin/env python
from __future__ import print_function
import optparse, sys
from py_compile import compile

parser = optparse.OptionParser()

(options, args) = parser.parse_args()

def compileandraise(fname):
    try:
        compile(fname, doraise=True)
    except Exception as e:
        tup = tuple(e)
        typ = tup[1]
        msg, info = tup[2]
        fname, line, col, lineasstr = info
        print(str(typ) + ":", msg, file=sys.stderr)
        print(str(fname) + ':' + str(line) + ':' + str(col) + ':' + lineasstr, file=sys.stderr)
        exit(1)



if not args:
    print("File name is needed!", file = sys.stderr)

for arg in args:
    compileandraise(arg)