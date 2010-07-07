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
import os.path

#frmtr = string.Formatter()
def getdir(*args):
    return os.path.join('/data/audio', *args)

class lwrdfltdict(defaultdict):
    def __setitem__(self, x, y):
        return defaultdict.__setitem__(self, x.lower(), y)
    
    def __getitem__(self, y):
        return defaultdict.__getitem__(self, y.lower())
    
    def __getattr__(self, x):
        if x in self:
            return self[x]
        else:
            return defaultdict.__getattr__(self, x)
    
    def __setattr__(self, x, y):
        if x in self:
            self[x] = y
        else:
            return defaultdict.__setattr__(self, x, y)
    
    def __call__(self, **kwargs):
        for k,v in kwargs.items():
            self[k] = v.format(**self)
    
    def pprint(self):
        """Print tag key=value pairs."""
        strings = []
        for key in self.keys():
            value = self[key]
            strings.append("{0:15}={1}".format(key, value))
        return "\n".join(strings)


# should really hand off the id3 objects with fname, fdir, fnum and not do this
# funny dict thing
def id3walk(dir = os.getcwd(), makechanges = False, ignoreerr = True):
    dir = os.path.expanduser(dir)
    if not os.path.exists(dir):
        raise SystemError, "Directory does not exist"
    for (fdir, ds, fs) in os.walk(dir):
        num = 0
        for f in sorted(fs):
            fpath = os.path.join(fdir, f)
            try:
                #id3 = ID3(f)
                eid3 = Leasyid3(fpath, usedefault=True)
            except ID3NoHeaderError, e:
                #print f, e
                if not ignoreerr:
                    yield f
                continue
            
            oldeid3fname = eid3.filename
            num += 1
            eid3.num = num
            eid3.dir = fdir
            #id3dict['num'] = num
            #id3dict['dir'] = fdir
            #id3dict['filename'] = f
            #id3dict.update(eid3)
            
            #yield id3dict
            oldcopy = dict(eid3)
            yield eid3
            
            #del id3dict['num']
            #newf = id3dict['filename']
            #del id3dict['filename']
            #newpath = os.path.join(fdir, newf)
            #del id3dict['dir']
            newf = os.path.basename(eid3.filename)
            newdir = eid3.dir
            #print "DIR:", eid3.dir
            #print "FNAME:", newf
            newpath = os.path.join(newdir, newf)
            #print "PATH:", newpath
            oldpath = os.path.join(fdir, f)
            
            needtosave = False
            for k,v in eid3.items():
                #print "KEY", k, "V", v
                if k not in oldcopy or v != oldcopy[k]:
                    print 'CHANGING',k,'to',v
                    needtosave = True
            
            fchanged = False
            try:
                fchanged = not os.path.samefile(newpath, oldpath)
            except OSError, e:
                if e.errno == 2:
                    fchanged = True
                else:
                    raise
            
            
            if fchanged:
                eid3.filename = newpath
                needtosave = True
                del eid3.dir
            else:
                eid3.filename = oldeid3fname
            
            if makechanges and needtosave:
                # need to rename to new filename
                print "Saving..."
                eid3.save()
                #print eid3.filename
                #print eid3.dir
            
            #if makechanges:
                ## need to rename to new filename
                #if not os.path.samefile(newpath, oldpath):
                    #try:
                        #os.rename(oldpath, newpath)
                    #except OSError, e:
                        #print e
                        #print "RENAME/MOVE FAILED"

def filesanitize(s):
    s = s.replace(':', '-')
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    s = s.replace(',', '')
    s = s.replace('!', '')
    return s

def id3format(dir = os.getcwd(), makechanges = False, ignoreerr = True,
                **kwargs):
    for f in id3walk(*args, **kwargs):
            for (k,v) in kwargs:
                f(k=v)
        
