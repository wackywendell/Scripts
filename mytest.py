print "Running my test!"

import os, re

class _TermColors(dict):
    """Gives easy access to ANSI color codes. Attempts to fall back to no color
    for certain TERM values. (Mostly stolen from IPython.)"""

    COLOR_TEMPLATES = (
        ("Black"       , "0;30"),
        ("Red"         , "0;31"),
        ("Green"       , "0;32"),
        ("Brown"       , "0;33"),
        ("Blue"        , "0;34"),
        ("Purple"      , "0;35"),
        ("Cyan"        , "0;36"),
        ("LightGray"   , "0;37"),
        ("DarkGray"    , "1;30"),
        ("LightRed"    , "1;31"),
        ("LightGreen"  , "1;32"),
        ("Yellow"      , "1;33"),
        ("LightBlue"   , "1;34"),
        ("LightPurple" , "1;35"),
        ("LightCyan"   , "1;36"),
        ("White"       , "1;37"),
        ("Bold"        , "1;1"),
        ("Normal"      , "0"),
    )

    NoColor = ''
    _base  = '\001\033[%sm\002'
    #_base  = r'\[\e[%sm\]'
    _simple = '\033[%sm'
    #_simple  = r'\[\e[%sm\]'

    def __init__(self, simple=False, nocolor = False):
        if not nocolor and os.environ.get('TERM') in ('xterm', 'xterm-color',
                'xterm-256color', 'linux', 'screen', 'screen-256color',
                'screen-bce'):
            if simple:
                self.update(dict([(k, self._simple % v) 
                            for k,v in self.COLOR_TEMPLATES]))
            else:
                self.update(dict([(k, self._base % v)
                            for k,v in self.COLOR_TEMPLATES]))
            
            for k,v in self.COLOR_TEMPLATES:
                self['B' + k] = self[k] + self['Bold']
        else:
            print("No colors, in terminal " + os.environ.get('TERM'))
            self.update(dict([(k, self.NoColor) for k,v in self.COLOR_TEMPLATES]))
    
    def splitter(self, txt, regexobj):
        splits = iter(regexobj.split(txt))
        for word in splits:
            sep = ''
            try:
                sep = splits.next()
            except StopIteration:
                pass
            yield (word, sep)
        return
    
    def wrap(self, txt, width=20):
        newtxt=[]
        nextline=""
        curlength=0
        cursep=''
        curcol = ''
        colorwords = (re.escape(v) for v in self.values() if v)
        #print(repr('([' + ",".join(colorwords) + '])'))
        colre = re.compile('(' + "|".join(colorwords) + '+)')
        spacere = re.compile(r'([ \t]+)')
        newlinere = re.compile(r'(\n)')
        for (line, lbreak) in self.splitter(txt, newlinere):
            linesplit = [(line, '')]
            if colorwords:
                linesplit = self.splitter(line, colre)
            for (colgroup, color) in linesplit:
                print(repr(colgroup + '---' + color))
                for (word, sep) in self.splitter(colgroup, spacere):
                    if curlength + len(cursep) + len(word) < width:
                        nextline += cursep + word
                        curlength += len(cursep) + len(word)
                        #print("; ".join((word, nextline, str(curlength))))
                    else:
                        newtxt.append(nextline)
                        nextline = word
                        curlength = len(word)
                    cursep = sep
                nextline += color
            newtxt.append(nextline)
            nextline = ''
            curlength = 0
        return '\n'.join(newtxt)
        #for line in "\n".split(txt):
            #if colorwords:
                #linesplit = colre.split(line)
            #else:
                #linesplit = [line]
            #linesplit = iter(linesplit)
            #for colgroup in linesplit:
                #try:
                    #curcol = linesplit.next()
                #except StopIterationError:
                    #curcol = ''
                #wordsplit = iter(spacere.split(colgroup))
                #for word in wordsplit:
                    #if(len(curline)):
                        

d = _TermColors(True)
t1 = 'abcdef '*13
t21 = d['Red']+'abcdef '+d['Normal']
t2 = d['BRed']+'abcdef '+d['Normal']
t3 = t2*13
colorwords = [re.escape(v) for v in d.values() if v]
crx = '(' + "|".join(colorwords) + '+)'
cre = re.compile(crx)


class f:
    def __enter__(self):
        print("entering now!")

    def __exit__(self, t, val, trce):
        print("exiting now!")
        if trce:
            print(t)
            print(val)
            global lasttrace
            lasttrace = trce
            print(trce)
            #print("Exception repressed.")
        return True

def g():    
    with f() as c:
        print("hi")
        print(x/2)

def h():
    print 'h2'
