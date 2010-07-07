from term import *

procs = ('thunderbird', 'firefox')

def getps():
    pids = []
    for proc in procs:
        pids.extend(pid(proc))
    return pids

for procname in procs:
    print "PROCESS:", procname
    for procid in pid(procname):
        print "\tID:", procid
        try:
            kill(procid, 15)
        except:
            pass

scl('pm-suspend')
