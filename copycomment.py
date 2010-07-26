#!/usr/bin/python

import pyexiv2
from optparse import OptionParser
from myspath import path

optparser = OptionParser()

(options, args) = optparser.parse_args()

print len(args)

lastdir = ''
nwithout=0

for f in args:
    dir = path().abspath()
    p = dir + f
    if len(args) > 1 and str(dir) != lastdir:
        lastdir = dir
        print dir
    try:
        img = pyexiv2.Image(f)
        img.readMetadata()
    except IOError as e:
        #print "FAILED READING!", e
        nwithout +=1
        continue
    if 'Iptc.Application2.Caption' in img.iptcKeys():
        print p.abspath()
        print 'CAPTION:', img['Iptc.Application2.Caption']
    else:
        nwithout +=1
        if nwithout % 100 == 0:
            print "%d pictures without captions..." % nwithout


print "%d pictures without captions..." % nwithout
