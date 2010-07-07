import mutagen
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.easyid3 import EasyID3
from collections import Mapping
from myspath import path
import os

class id3manager(Mapping):
    _transdict = {
        'title' : 'TIT2',
        'track' : 'TRCK',
        'artist' : 'TPE1',
        'album' : 'TALB',
        'genre' : 'TCON'
    }
    
    def __init__(self, id3file):
        if isinstance(id3file, path):
            id3file = str(id3file)
        if isinstance(id3file, str):
            id3file = ID3(id3file)
        self._id3 = id3file
        self._keydict = {}
        for key in id3file.keys():
            self._keydict[key.upper()] = key
        self._oldfilename = None
        self.changedkeys = set()
    def __getitem__(self, key):
        if key in self._transdict:
            key = self._transdict[key]
        try:
            return self._id3[key].text[0]
        except AttributeError:
            return self._id3[key]
                
    
    def __setitem__(self, key, value):
        origval = value
        if key in self._transdict:
            key = self._transdict[key]
        if hasattr(mutagen.id3, key):
            if isinstance(value, (str, unicode, list)):
                cls = getattr(mutagen.id3, key)
                value = cls(encoding=3,text = value)
                #print 'lst', repr(value)
        if key in self._id3:
            oldval = self._id3.__getitem__(key)
            if not value == oldval: # for some reason, '!=' doesn't work here
                #print repr(value), repr(oldval)
                self.changedkeys.add(key)
        else:
            self.changedkeys.add(key)
        return self._id3.__setitem__(key, value)
    
    @property
    def filename(self):
        "The filename can be set with a path object or string, and is returned as a path object"
        return path(self._id3.filename)
    
    @filename.setter
    def filename(self, val):
        p = path(val).expanduser().realpath()
        if not self._oldfilename:
            self._oldfilename = path(self._id3.filename)
        self._id3.filename = str(val)
    
    def __iter__(self):
        return self._id3.__iter__()
    
    def __len__(self):
        return self._id3.__len__()
    
    def __str__(self):
        pprinted = [self[k].pprint() for k in self.keys()]
        return "<id3manager: " + ",".join(pprinted) + '>'
    
    def save(self):
        if self._oldfilename:
            self._oldfilename.move(self._id3.filename)
            self._oldfilename = None
        retval = self._id3.save()
        self.savedkeys = set()
        return retval
    
    def pprint(self):
        return "Filename=" + str(self._id3.filename)  + '\n' + self._id3.pprint()

def id3walk(dir = path.cwd(), makechanges = False, ignoreerr = True, printout = True):
    """Walks through a directory, yielding all files that can be read as ID3 files.
    
    makechanges: id3walk will save afterwards if true
    ignoreerr: with this option, files that cannot be read are ignored and skipped; without this option, files that cannot be read are yielded as path objects.
    """
    origwd = path.cwd()
    dir = path(dir).expanduser().realpath()
    if not dir.isdir():
        raise SystemError, "Directory %s does not exist" % str(dir)
    dir.chdir()
    for fpath in sorted(dir.getfiles(descend = True)):
        if fpath.extension.lower() == 'partial':
            continue
        try:
            #id3 = ID3(f)
            eid3 = id3manager(fpath)
        except ID3NoHeaderError, e:
            if not ignoreerr:
                yield fpath
            continue

        yield eid3
        
        changed = []
        eid3.filename = eid3.filename.expanduser()
        newfname = eid3.filename.realpath()
        if fpath.realpath() != newfname:
            #changed.append("Filename (" + str(newfname) + ")")
            changed.append("Filename")
        for k in eid3.changedkeys:
            changed.append(k)
        if changed and printout:
            print "Changed " + ",".join(changed)
        if makechanges and changed:
            if printout:
                print "Saving..."
            eid3.save()
    
    origwd.chdir()

def filesanitize(s):
    cls = s.__class__
    s = str(s)
    s = s.replace(':', '-')
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    s = s.replace(',', '')
    s = s.replace('!', '')
    return cls(s)

#id3fn=path("~/scripts/test/rlab604.mp3").expanduser()
#id3fn[:-1].chdir()
#id=id3manager(id3fn)
def prntloc(dir='.'):
    dir = path(dir)
    for f in id3walk(dir):
        print(f.pprint())
        print('='*70)
#id2=ID3(id3fn)
#id3=EasyID3(id3fn)
