#!/usr/bin/python

from __future__ import print_function

import re
from id3man import *
from myspath import path

mainbasedir = path('/home/wendell/Music/gpodder/')
mainfinaldir = path('/home/wendell/Music/podcast')

class Directory(object):
    members = []
    
    def __init__(self, title, basedir=None, finaldir=None, fix=None):
        title = self.title = title or unicode(basedir[-1])
        self.basedir = basedir or mainbasedir + filesanitize(title)
        self.basedir = path(self.basedir)
        self.finaldir = finaldir or mainfinaldir + unicode(filesanitize(title))
        self.finaldir = path(self.finaldir)
        self.album = title
        self.artist = title
        self.genre = 'Podcast'
        self.experimental = False
        if fix:
            self.fix = fix
        self.members.append(self)
    
    def run(self, makechanges=True, ignoreerr=True, printout=True):
        print('='*72)
        if self.experimental:
            makechanges = False
        if printout:
            print('***', unicode(self.title) + '...')
        copycover(self.basedir, self.finaldir)
        for f in id3walk(self.basedir, makechanges, ignoreerr, printout):
            self.fix(f, printout)
    
    def runold(self, makechanges = False, ignoreerr=True, printout=True):
        basedir = self.basedir
        self.basedir = self.finaldir
        self.run(makechanges, ignoreerr, printout)
        self.basedir = basedir
    
    @classmethod
    def runall(cls, makechanges=True, ignoreerr=True, printout=True):
        for member in cls.members:
            member.run(makechanges, ignoreerr, printout)
    
    def newfix(self, func):
        self.fix = lambda *a, **kw: func(self, *a, **kw)
    
    def fix(self, f, printout=True):
        self.defaultfix(f, printout)
    
    def defaultfix(self, f, printout = True):
        printout and print('-'*72)
        printout and print(f.filename)
        printout and print("Title:   ", f['title'])
        if self.artist and f['artist'] != self.artist:
            f['artist'] = self.artist
            printout and print('Artist:  ', f['artist'])
        if self.album and f['album'] != self.album:
            f['album'] = self.album
            printout and print('Album:  ', f['album'])
        f['genre'] = self.genre
        f.filename = self.finaldir + f.filename[-1]

class Librivox(Directory):
    def __init__(self, basedir, finaldir=None, title=None, fix=None):
        Directory.__init__(self, basedir, finaldir, title, fix)
        self.genre = 'Audiobook'
    
    def defaultfix(self, f, printout=True):
        Directory.defaultfix(self, f, printout)
        if str(f['artist']) != 'Librivox':
            if printout:
                print("artist:", str(f['artist']))
            f['TOPE'] = str(f['artist'])
            f['artist'] = 'Librivox'



def titlefitter(strng):
    title = None
    num = None
    disc = None
    strng = strng.strip()
    m = re.match(r'(\d+)[ -]+(\d+)[ :-]+(.+)', strng)
    if m:
        #print 3,m
        disc,num,title = m.groups()
        title = title.strip()
        return (title,num,disc)
    m = re.match(r'(\d+)[ :-]*(.+)', strng)
    if m:
        #print m
        #print 2,m.groups()
        num,title = m.groups()
        title = title.strip()
        return (title,num,"")
    else:
        return None
        
def copycover(dir1, dir2):
    cvr = path(dir1) + "cover"
    fnlcvr = path(dir2) + "cover"
    if cvr.isfile() and not fnlcvr.isfile():
        cvr.copy(dir2, True)

inourtime = Directory('In Our Time')
inourtime.basedir = mainbasedir + "In Our Time With Melvyn Bragg"
inourtime.finaldir = mainfinaldir + "Melvyn_Bragg/In_Our_Time"
inourtime.artist = 'Melvyn Bragg'
inourtime.album = 'In Our Time'

bob = Directory('History According to Bob')
bob.basedir = mainbasedir + "History According to Bob (2)"
bob.finaldir = mainfinaldir + "Bob/History_According_to_Bob"
bob.genre = 'Podcast'
bob.album = 'History According to Bob'
bob.artist = 'Bob'

thinking = Directory('Thinking Allowed',
                path("/home/wendell/Music/gpodder/Thinking Allowed"),
                path("/home/wendell/Music/podcast/Thinking_Allowed"))
thinking.artist = 'BBC'
thinking.album = 'Thinking Allowed'

thor = Directory('The History of Rome',
    path("/data/mp3/gpodder/The History of Rome/"),
    path("/home/wendell/Music/podcast/Mike_Duncan/The_History_Of_Rome"))
thor.artist = 'Mike Duncan'
thor.album = 'Rome'
thor.genre = 'Podcast'
@thor.newfix
def fix(self, f, printout=True):
    self.defaultfix(f, printout)
    t = f['title']
    t = t.replace('-The History of Rome', '')
    t = t.replace(': ','-')
    t = t.replace('- ','-')
    t = t.replace(' -','-')
    if t[:4] == 'Thor':
        t = 'THOR' + t[4:]
    if (t[:5]).upper() == 'THOR ':
        t = t[5:]
    #else: print(t[:5])
    title, num,disc = titlefitter(t)
    if int(num) == 666 or int(num) == 66:
        num = '66'
        if '666' not in title:
            title = '666: ' + title
    printout and print("num,disc:", repr((num,disc)))
    f['title'] = "%03d-%s" % (int(num), title)
    if title[1] == '-':
        f['title'] = "%03d%s" % (int(num), title)
    f['track'] = str(num)
    #print title, num, disc
    newf = filesanitize(str(f['title'])) + '.mp3'
    printout and print("new title:", f['title'])
    f.filename = self.finaldir + newf
    printout and print("new filename:", f.filename)
        
norman= Directory('Norman Centuries',
    path("/home/wendell/Music/gpodder/Norman Centuries | A Norman History Podcast by Lars Brownworth (2)"),
    path("/home/wendell/Music/podcast/Lars_Brownworth/Norman_Centuries"))
norman.artist = 'Lars Brownworth'
norman.album = 'Norman Centuries'

byzantine = Directory('12 Byzantine Rulers',
    path("/home/wendell/Music/gpodder/12 Byzantine Rulers_ The History of The Byzantine Empire"),
    path("/home/wendell/Music/podcast/Lars_Brownworth/Byzantine_Rulers"))
byzantine.artist = 'Lars Brownworth'


fooc=Directory('From Our Own Correspondent',
    path("/data/mp3/gpodder/From Our Own Correspondent"),
    path("/data/mp3/podcast/From_Our_Own_Correspondent"))
fooc.artist = 'BBC'
@fooc.newfix
def fix(self, f, printout=True):
    self.defaultfix(f, printout)
    match = re.match(r"fooc_(\d{4})(\d{2})(\d{2})-\d+.*\.mp3", f.filename[-1])
    if match:
        yr, mnth, day = match.groups()
        yr = int(yr) % 1000
        mnth = int(mnth)
        day = int(day)
        f['title'] = "FOOC {0:02d}-{1:02d}-{2:02d}".format(yr, mnth, day)
        f.filename = self.finaldir + f.filename[-1]
        
        printout and print(f['title'])
        printout and print(f.filename)
        tnum = unicode((yr-10)*366 + mnth * 31 + day)
        if not f.get('track','') == tnum:
            f['track'] = tnum
            printout and print('Track number', f['track'])
    else:
        printout and print("MATCH FAILED!!")

dancarlin=Directory('Hardcore History', 
    r"/data/mp3/gpodder/Dan Carlin's Hardcore History (2)/",
    r"/data/mp3/podcast/Dan_Carlin")
dancarlin.artist = 'Dan Carlin'

pri=Directory('TTBOOK',
    path(r"/data/mp3/gpodder/PRI_ To the Best of Our Knowledge Podcast/"),
    finaldir = path(r"/data/mp3/podcast/PRI"))
pri.artist = 'PRI'
pri.album = 'To the Best of Our Knowledge'

radiolab=Directory('Radiolab',
    path(r"/data/mp3/gpodder/WNYC's Radio Lab/"),
    path(r"/data/mp3/podcast/Radiolab"))

npr=Directory('NPR',
    path(r"/data/mp3/gpodder/NPR_ Science Friday Podcast/"),
    r"/data/mp3/podcast/NPR")
npr.album = 'Science Friday'

kermode = Directory('Kermode',
    '/home/wendell/Music/gpodder/Kermode',
    '/home/wendell/Music/podcast/Kermode')

nature = Directory('Nature',
    "/home/wendell/Music/gpodder/Nature Podcast",
    "/home/wendell/Music/podcast/Nature")
nature.album = 'Nature Podcast'
        
if __name__ == "__main__": #and False:
    Directory.runall()