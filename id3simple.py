#!/usr/bin/python

import re
from id3man import *
from myspath import path


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

def scifi(n):
    alb = 'Sci-Fi Shorts ' + str(n)
    libr('/data/audio/audiobook/scifi_collection_'+str(n), alb)

def myst(n):
    alb = 'Mystery Shorts ' + str(n)
    libr('/data/audio/audiobook/mystery_collection_'+str(n), alb)
    
def sherholm(makechanges = False):
    dr = '/data/audio/audiobook'
    
    
    for f in id3walk(dr, makechanges, True):
        if 'Sherlock' not in f.dir:
            continue
        print('-'*40)
        #print(f.pprint())
        #print(f.filename)
        print(f['title'])
        if f['artist'] != 'Sir Arthur Conan Doyle':
            f['tope'] = f['artist']
            f['artist'] = 'Sir Arthur Conan Doyle'
        startstr = 'The Adventure Of '.lower()
        if f['title'][:len(startstr)].lower() == startstr:
            f['title'] = f['title'][len(startstr):].strip()
        
        #m = re.match(r'(\d*) *- *(\d*) *(.*)',f['title'])
        #
        #if len(splits) > 3 or len(splits) < 2:
            #raise KeyError, "Expected title of form '# - TITLE' or '#-# - title'"
        #title = splits[-1]
        #num = splits[-2]
        #if len(splits) == 3:
            #f['TPOS'] = splits[0]
        try:
            f['title'], f['tracknum'], disc = titlefitter(f['title'])
            if disc:
                f['TPOS'] = disc
        except TypeError:
            pass
        f['genre'] = 'Audiobook'
        lastf = f
    
    
    
def libshorts(makechanges = False):
    dr='/home/wendell/Music/gpodder/Classic Short Stories from LibriVox [Unabridged] (2)'
    finaldir = '/home/wendell/Music/audiobook/Classic_Short_Stories'
    alb = 'Best Short Stories' 
    libr(dr,finaldir,alb,makechanges)

lastf = None

def libr(dr, finaldir, alb, makechanges = True, ignoreerr = True):
    for f in id3walk(dr, makechanges, ignoreerr):
        print('-'*40)
        #print(f.pprint())
        #print(f.filename)
        print(f['title'])
        if str(f['artist']) != 'Librivox':
            print "artist:", str(f['artist'])
            f['TOPE'] = str(f['artist'])
            f['artist'] = 'Librivox'
        f['genre'] = 'Audiobook'
        f['album'] = alb
        f.filename = path(finaldir) + path(f.filename)[-1]
    #print dir(lastf)
        

def slowg():
    dir = '/data/audio/gpodder/d7bd50135ba90812eb08a217197bf91d'
    for f in id3walk(dir, True):
        print('-'*40)
        print(f['title'])
        f['title'] = f['title'].replace('Slow German #','')
        f['title'] = f['title'].replace(': ','-')
        f['title'] = f['title'].replace(':','-')
        if f['title'][2] == '-':
            f['title'] = '0'+f['title']
        try:
            tr=int(f['title'][:3])
            f['trck']=str(tr)
        except ValueError:
            pass

def inourtime(fullrun=True):
    #dir = '/data/mp3/podcast/Mike Duncan/The History Of Rome'
    dir = path("/home/wendell/Music/gpodder/In Our Time With Melvyn Bragg")
    finaldir = path("/home/wendell/Music/podcast/Melvyn_Bragg/In_Our_Time")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        t = f['title']
        f['artist'] = 'Melvyn Bragg'
        f['album'] = 'In Our Time'
        f['genre'] = 'Podcast'
        #print title, num, disc
        f.filename = finaldir +f.filename[-1]
        print "new filename:", f.filename

def thinking(fullrun=True):
    #dir = '/data/mp3/podcast/Mike Duncan/The History Of Rome'
    dir = path("/home/wendell/Music/gpodder/Thinking Allowed")
    finaldir = path("/home/wendell/Music/podcast/Thinking_Allowed")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        t = f['title']
        f['artist'] = 'BBC'
        f['album'] = 'Thinking Allowed'
        f['genre'] = 'Podcast'
        #print title, num, disc
        f.filename = finaldir +f.filename[-1]
        print "new filename:", f.filename

def thor(fullrun=True):
    #dir = '/data/mp3/podcast/Mike Duncan/The History Of Rome'
    dir = path("/data/mp3/gpodder/The History of Rome/")
    finaldir = path("/home/wendell/Music/podcast/Mike_Duncan/The_History_Of_Rome")
    copycover(dir, finaldir)
    for f in id3walk(dir, fullrun):
        print('-'*40)
        print(f['title'])
        print(f.filename)
        t = f['title']
        f['artist'] = 'Mike Duncan'
        f['album'] = 'Rome'
        f['genre'] = 'Podcast'
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
        print "num,disc:", repr((num,disc))
        f['title'] = "%02d-%s" % (int(num), title)
        if title[1] == '-':
            f['title'] = "%02d%s" % (int(num), title)
        f['track'] = str(num)
        #print title, num, disc
        newf = filesanitize(str(f['title'])) + '.mp3'
        print "new title:", f['title']
        f.filename = finaldir + newf
        print "new filename:", f.filename
        
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
        print "new title:", f['title']
        f.filename = finaldir + f.filename[-1]
        print "new filename:", f.filename

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
        print "new title:", f['title']
        f.filename = finaldir + f.filename[-1]
        print "new filename:", f.filename


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
        print "new title:", f['title']
        f.filename = finaldir + f.filename[-1]
        print "new filename:", f.filename
        
def fooc(makechanges = False):
    finaldir = path("/data/mp3/podcast/From_Our_Own_Correspondent")
    dir = path("/data/mp3/gpodder/From Our Own Correspondent")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print "-"*70
        print f.filename
        print f['title']
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
            print f['title']
            print f.filename
        else:
            print "MATCH FAILED!!"

def dancarlin(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/Dan_Carlin")
    dir = path(r"/data/mp3/gpodder/Dan Carlin's Hardcore History (2)/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print "-"*70
        print f.filename
        try:
            print f['title'], f['album']
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
        print "-"*70
        print f.filename
        print f['title'], f['album']
        f['album'] = 'To the Best of Our Knowledge'
        f['artist'] = 'PRI'
        f.filename = finaldir + f.filename[-1]

def radiolab(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/Radiolab")
    dir = path(r"/data/mp3/gpodder/WNYC's Radio Lab/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print "-"*70
        print f.filename
        print f['title'], f['album']
        f['album'] = 'Radiolab'
        f['artist'] = 'Radiolab'
        f.filename = finaldir + f.filename[-1]

def npr(makechanges = False):
    finaldir = path(r"/data/mp3/podcast/NPR")
    dir = path(r"/data/mp3/gpodder/NPR_ Science Friday Podcast/")
    if makechanges:
        copycover(dir, finaldir)
    for f in id3walk(dir, makechanges):
        print "-"*70
        print f.filename
        print f['title'], f['album']
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
        print "new filename:", f.filename
        

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
        print "new filename:", f.filename

if __name__ == "__main__": #and False:
    div = '='*30 + '\n'
    print div, "History of Rome..."
    thor(True)
    print div, "FOOC..."
    fooc(True)
    print div, "Dan Carlin..."
    dancarlin(True)
    print div, "PRI..."
    pri(True)
    print div, "NPR..."
    npr(True)
    print div, "Radio Lab..."
    radiolab(True)
    print div, "Bob..."
    bob(True)
    print div, "Norman Centuries..."
    norman(True)
    print div, "12 Byzantine Rulers..."
    byzantine(True)
    print div, "Shorts..."
    libshorts(True)
    print div, "In Our Time..."
    inourtime(True)
    print div, "Thinking Allowed..."
    thinking(True)
    print div, "Kermode..."
    kermode(True)
    print div, "Nature..."
    nature(True)
    
