#!/usr/bin/python2.6

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from leasyid3 import Leasyid3
from mutagen.id3 import ID3NoHeaderError
from sys import argv
from collections import defaultdict
import string

import os

usage = "id3fix.py TAG PATTERN\n"

if len(argv) != 3:
    print usage
    exit()

tagname = argv[1]
tagtempl = argv[2]

frmtr = string.Formatter()

class lwrdfltdict(defaultdict):
    def __setitem__(self, x, y):
        return defaultdict.__setitem__(self, x.lower(), y)
    
    def __getitem__(self, y):
        return defaultdict.__getitem__(self, y.lower())

for (dir, ds, fs) in os.walk('.'):
    num = 0
    for f in fs:
        try:
            id3 = ID3(f)
            eid3 = Leasyid3(f, usedefault=True)
        except ID3NoHeaderError, e:
            print f, e
        
        id3dict = lwrdfltdict(lambda: '')
        num += 1
        id3dict['num'] = num
        id3dict.update(eid3)
        #print id3dict
        #for k,v in id3.items():
            #id3dict[k] = str(v[0])
        
        print f
        print eid3.pprint()
        ftag = eid3[tagname]
        print "old " + tagname + ":", ftag

        newtag = frmtr.vformat(tagtempl,[],eid3)
        print "new:", newtag
        
        eid3[tagname] = newtag
        eid3.save()
        
        ## can't just save to the id3 dict, which is annoying, 
        ## have to get the class
        #tagclass = mutagen.id3.__dict__[tagname.upper()]
        ## make an object from the class
        #newtagobj = tagclass(encoding=3,text=newtag)
        
        ##now put it in the object and save
        #id3.add(newtagobj)