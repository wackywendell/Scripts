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
        self.finaldir = finaldir or mainfinaldir + unicode(filesanitize(title))
        self.album = title
        self.artist = title
        self.genre = 'Podcast'
        self.experimental = False
        if fix:
            self.fix = fix
        self.members.append(self)
    
    def run(self, makechanges=True, ignoreerr=True, printout=True):
        print('-'*72)
        if self.experimental:
            makechanges = False
        if printout:
            print('***', unicode(self.title) + '...')
        copycover(self.basedir, self.finaldir)
        for f in id3walk(self.basedir, makechanges, ignoreerr, printout):
            print("Calling:", repr(f), repr(printout))
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
    cvr = dir1 + "cover"
    fnlcvr = dir2 + "cover"
    if cvr.isfile() and not fnlcvr.isfile():
        cvr.copy(dir2, True)

inourtime = Directory('In Our Time')
inourtime.basedir = mainbasedir + "In Our Time With Melvyn Bragg"
inourtime.finaldir = mainfinaldir + "Melvyn_Bragg/In_Our_Time"
inourtime.artist = 'Melvyn Bragg'
inourtime.album = 'In Our Time'
inourtime.experimental = True

bob = Directory('History According to Bob')
bob.basedir = mainbasedir + "History According to Bob (2)"
bob.finaldir = mainfinaldir + "Bob/History_According_to_Bob"
bob.genre = 'Podcast'
bob.album = 'History According to Bob'
bob.artist = 'Bob'
bob.experimental = True

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
    print(repr(self), repr(f), repr(printout))
    t = f['Title']
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
    f['title'] = "%02d-%s" % (int(num), title)
    if title[1] == '-':
        f['title'] = "%02d%s" % (int(num), title)
    f['track'] = str(num)
    #print title, num, disc
    newf = filesanitize(str(f['title'])) + '.mp3'
    printout and print("new title:", f['title'])
    f.filename = self.finaldir + newf
    printout and print("new filename:", f.filename)
        

def bob(fullrun=False):
    #dir = '/data/mp3/podcast/Mike Duncan/The History Of Rome'
    dir = path("/data/mp3/gpodder/History According to Bob (2)")
    finaldir = path("/home/wendell/Music/podcast/Bob/History_According_to_Bob")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        f['genre'] = 'Podcast'
        
        t = f['title']
        f['artist'] = 'Bob'
        f['album'] = 'History According to Bob'
        #else: print(t[:5])
        #title, num,disc = titlefitter(t)
        print("new title:", f['title'])
        f.filename = finaldir + f.filename[-1]
        print("new filename:", f.filename)

def norman(fullrun=False):
    #dir = '/data/mp3/podcast/Mike Duncan/The History Of Rome'
    dir = path("/home/wendell/Music/gpodder/Norman Centuries | A Norman History Podcast by Lars Brownworth (2)")
    finaldir = path("/home/wendell/Music/podcast/Lars_Brownworth/Norman_Centuries")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        f['genre'] = 'Podcast'
        
        t = f['title']
        f['artist'] = 'Lars Brownworth'
        f['album'] = 'Norman Centuries'
        #else: print(t[:5])
        #title, num,disc = titlefitter(t)
        print("new title:", f['title'])
        f.filename = finaldir + f.filename[-1]
        print("new filename:", f.filename)


def byzantine(fullrun=False):
    dir = path("/home/wendell/Music/gpodder/12 Byzantine Rulers_ The History of The Byzantine Empire")
    finaldir = path("/home/wendell/Music/podcast/Lars_Brownworth/Byzantine_Rulers")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        f['genre'] = 'Podcast'
        
        t = f['title']
        f['artist'] = 'Lars Brownworth'
        f['album'] = '12 Byzantine Rulers'
        #else: print(t[:5])
        #title, num,disc = titlefitter(t)
        print("new title:", f['title'])
        f.filename = finaldir + f.filename[-1]
        print("new filename:", f.filename)
        
def fooc(makechanges = False):
    finaldir = path("/data/mp3/podcast/From_Our_Own_Correspondent")
    dir = path("/data/mp3/gpodder/From Our Own Correspondent")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print("-"*70)
        print(f.filename)
        print(f['title'])
        #t = f['title']
        #t = subremove(t, "FOOC:").strip()
        #t = subremove(t, "BBC Radio 4").strip()
        #t = subremove(t, ",").strip()
        #print t
        match = re.match(r"fooc_(\d{4})(\d{2})(\d{2})-\d+.*\.mp3", f.filename[-1])
        f['album'] = 'From Our Own Correspondent'
        f['artist'] = 'BBC Radio'
        if match:
            yr, mnth, day = match.groups()
            yr = yr [-2:] # drop the '20' part of the year
            f['title'] = "FOOC {0}-{1}-{2}".format(yr, mnth, day)
            f.filename = finaldir + f.filename[-1]
            print(f['title'])
            print(f.filename)
        else:
            print("MATCH FAILED!!")

def dancarlin(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/Dan_Carlin")
    dir = path(r"/data/mp3/gpodder/Dan Carlin's Hardcore History (2)/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print("-"*70)
        print(f.filename)
        try:
            print(f['title'], f['album'])
        except Exception:
            pass
        f['album'] = 'Hardcore History'
        f['artist'] = 'Dan Carlin'
        f.filename = finaldir + f.filename[-1]

def pri(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/PRI")
    dir = path(r"/data/mp3/gpodder/PRI_ To the Best of Our Knowledge Podcast/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print("-"*70)
        print(f.filename)
        print(f['title'], f['album'])
        f['album'] = 'To the Best of Our Knowledge'
        f['artist'] = 'PRI'
        f.filename = finaldir + f.filename[-1]

def radiolab(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/Radiolab")
    dir = path(r"/data/mp3/gpodder/WNYC's Radio Lab/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print("-"*70)
        print(f.filename)
        print(f['title'], f['album'])
        f['album'] = 'Radiolab'
        f['artist'] = 'Radiolab'
        f.filename = finaldir + f.filename[-1]

def npr(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/NPR")
    dir = path(r"/data/mp3/gpodder/NPR_ Science Friday Podcast/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print("-"*70)
        print(f.filename)
        print(f['title'], f['album'])
        f['album'] = 'Science Friday'
        f['artist'] = 'NPR'
        f.filename = finaldir + f.filename[-1]

def subremove(s, sub):
    l = len(sub)
    if s[:l] == sub:
        return s[l:]
    else:
        return s


def kermode(fullrun=False):
    dir = path("/home/wendell/Music/gpodder/Kermode")
    finaldir = path("/home/wendell/Music/podcast/Kermode")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        f['genre'] = 'Podcast'
        
        t = f['title']
        f['artist'] = 'Kermode'
        f['album'] = 'Kermode'
        #else: print(t[:5])
        #title, num,disc = titlefitter(t)
        f.filename = finaldir + f.filename[-1]
        print("new filename:", f.filename)
        

def nature(fullrun=False):
    dir = path("/home/wendell/Music/gpodder/Nature Podcast")
    finaldir = path("/home/wendell/Music/podcast/Nature")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        f['genre'] = 'Podcast'
        
        t = f['title']
        f['artist'] = 'Nature'
        f['album'] = 'Nature Podcast'
        #else: print(t[:5])
        #title, num,disc = titlefitter(t)
        f.filename = finaldir + f.filename[-1]
        print("new filename:", f.filename)

if __name__ == "__main__": #and False:
    Directory.runall()
    
    
    exit()
    div = '='*30 + '\n'
    print(div, "History of Rome...")
    thor(True)
    print(div, "FOOC...")
    fooc(True)
    print(div, "Dan Carlin...")
    dancarlin(True)
    print(div, "PRI...")
    pri(True)
    print(div, "NPR...")
    npr(True)
    print(div, "Radio Lab...")
    radiolab(True)
    print(div, "Bob...")
    bob(True)
    print(div, "Norman Centuries...")
    norman(True)
    print(div, "12 Byzantine Rulers...")
    byzantine(True)
    print(div, "Shorts...")
    libshorts(True)
    print(div, "In Our Time...")
    inourtime(True)
    print(div, "Thinking Allowed...")
    thinking(True)
    print(div, "Kermode...")
    kermode(True)
    print(div, "Nature...")
    nature(True)
    
