#!/usr/bin/python3

import os, os.path
from subprocess import Popen, PIPE

def getprocs():
    fs = os.listdir('/proc')
    proclist = []
    for f in fs:
        try:
            int(f)
            proclist.append(f)
        except ValueError:
            pass
    
    procpairs = []
    
    for f in proclist:
        with open(os.path.join('/proc',f,'cmdline')) as cmdf:
            cmd = cmdf.read()
            cmd = cmd.strip().strip('\x00').split('\x00')
            exc = cmd[0]
            args = cmd[1:]
            procpairs.append((int(f),exc,args))
    
    return procpairs
    

def getwindows():
    wmproc = Popen("wmctrl -lp", shell=True,stdout=PIPE)
    wmoutb = wmproc.communicate()[0]
    wmout = wmoutb.decode()
    #print(type(wmout), "wmout:",wmout)
    wmoutlines = wmout.split('\n')
    #print(type(wmoutlines), "wmoutlines:",wmoutlines)
    
    fout = []
    
    for l in wmoutlines:
        fields = [f for f in l.split(" ") if f]
        if len(fields) < 3:
            continue
        
        (winid,sep,rest) = l.partition(' ')
        (desktop,sep,rest) = rest.strip().partition(' ')
        (pid,sep,rest) = rest.strip().partition(' ')
        (usr,sep,title) = rest.strip().partition(' ')
        
        lout = (int(pid), winid, usr, int(desktop), title)
        fout.append(lout)
    
    return fout

print(getwindows())