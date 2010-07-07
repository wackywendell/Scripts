#!/usr/bin/python

# right now this opens about 60 threads, which is WAY too many. Not allowed.
# see bottom to enable; currently disabled.

import ldap
import threading
from ldapfuncs import *

batchsize=10

print "Initializing..."
l=ldap.initialize("ldap://ldap.dartmouth.edu")
print "binding..."
l.simple_bind_s("dc=dartmouth,dc=edu","")
print "binding done"
# r = l.sqearch_s(
  # "CN=ANYCOMPUTER,CN=Computers,DC=dartmouth,DC=edu",
  # ldap.SCOPE_SUBTREE, # this is the default of ldapsearch
  # "(objectClass=*)"
# )
alpha="abcdefghijklmnopqrstuvwxyz"
# alpha="evwy. "
nums="1234567890"

def testcls(s):
    try:
        return s[0]=="'" and s[1] in nums and s[2] in nums
    except IndexError:
        return False

def batch(lst, size):
    b=[]
    loc=0
    while len(lst) > loc:
        b.append(lst[loc:loc+size])
        loc+=size
    return b

class getqueries(threading.Thread):
    def __init__(self, qs, trkr):
        threading.Thread.__init__(self)
        self.queries=qs
        self.tracker=trkr
        print self.getName() + " initializing"
    def run(self):
        self.l=ldap.initialize("ldap://ldap.dartmouth.edu")
        self.l.simple_bind_s("dc=dartmouth,dc=edu","")
        for q in self.queries:
            ps=queryname(q, self.l)
            for p in ps:
                self.tracker.update(p)

class tracker:
    def __init__(self):
        self.pcount=0
        self.people=set()
        self.lock=threading.Lock()
    def update(self, p):
            #~ print p
            self.lock.acquire()
            #~ print p.email
            #~ print p.cls
            if p.email and testcls(p.cls):
                self.people.add(p)
                self.pcount+=1
                thr=threading.currentThread()
                if self.pcount % 20 == 0:
                    print "%4d, %s, %s" % (self.pcount, str(p.email),
                                thr.getName())
            self.lock.release()

def queries():
    for a in alpha:
        for b in alpha:
            yield ("(&(CN=" + a + "*)(SN=" + b + "*)" +
                            "(eduPersonAffiliation=student))")
    

def main():
    trk = tracker()
    allqs = list(queries())
    groupedqs = batch(allqs, batchsize)
    
    thrds = [getqueries(lst, trk) for lst in groupedqs]
    
    print "running..."
    for t in thrds:
        t.start()
        
    print "joining..."
    for t in thrds:
        t.join()
    
    print "done joining, making list"
    

    print "making list"
    emaillst=[p.email for p in trk.people]
    emaillst.sort()
    emailstr="\n".join(emaillst)
    
    print "writing file"
    f=open("/data/wendell/college/campusemails.txt","w")
    f.write(emailstr)
    f.close()

if __name__ == "__main__":
    print "ldapdl.py MAIN"
    #~ main()
