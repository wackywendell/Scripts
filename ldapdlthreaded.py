#!/usr/bin/python
import ldap
import threading

numthreads=4

l=ldap.initialize("ldap://ldap.dartmouth.edu")
l.simple_bind_s("dc=dartmouth,dc=edu","")
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
        self.tot = len(self.queries)
        self.cur = 0
        self.tracker=trkr
        print self.getName() + " initializing"
    def run(self):
        self.l=ldap.initialize("ldap://ldap.dartmouth.edu")
        self.l.simple_bind_s("dc=dartmouth,dc=edu","")
        for q in self.queries:
            self.cur += 1
            ps=queryname(q, self.l)
            for p in ps:
                self.tracker.update(p, self.cur, self.tot)

class tracker:
    def __init__(self):
        self.pcount=0
        self.people=set()
        self.lock=threading.Lock()
    def update(self, p, n, tot):
            #~ print p
            self.lock.acquire()
            #~ print p.email
            #~ print p.cls
            if p.email and testcls(p.cls):
                self.people.add(p)
                self.pcount+=1
                thr=threading.currentThread()
                threadstr = "%4d/%4d" % (n, tot)
                if self.pcount % 20 == 0:
                    print "%4d, %50s, %10s (%s)" % (self.pcount, str(p.email),
                                thr.getName(), threadstr)
            self.lock.release()

def queryname(strng, ld):
    q=ld.search_s("dc=dartmouth,dc=edu",2,strng)
    return [person(p) for p in q]
    # return q

def searchstu(strng,yr):
    return queryname("(&(CN="+strng+"*)(dndDeptclass="+yr+
                            ")(eduPersonAffiliation=student))")

ldinternal = None

def getld():
    try:
        if ldinternal:
            return ldinternal
    except:
        pass
    ldinternal = ldap.initialize("ldap://ldap.dartmouth.edu")
    ldinternal.simple_bind_s("dc=dartmouth,dc=edu","")
    return ldinternal

def myquery(ld=None, **kwargs):
    if not ld:
        ld = getld()
    q="(&"
    for (k,v) in kwargs.iteritems():
        q += "(" + str(k) + "=" + str(v) + ")"
    q += ")"
    print q
    return ld.search_s("dc=dartmouth,dc=edu",2,q)

class person:
    def __init__(self, obj):
        d=obj[1]
        self.name  = d.get('cn',[""])[0]
        self.nicks = d.get('nickname',[""])[0]
        self.given = d.get('givenName',[""])[0]
        self.email = d.get('mail',[""])[0]
        self.cls   = d.get('dndDeptclass',[""])[0]
        self.affil = d.get('eduPersonAffiliation',[""])[0]

def queries():
    for a in alpha:
        for b in alpha:
            yield ("(&(CN=" + a + "*)(SN=" + b + "*)" +
                            "(eduPersonAffiliation=student))")
    

def main():
    trk = tracker()
    allqs = list(queries())
    groupedqs = batch(allqs, len(allqs)/numthreads + 1)
    
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
    main()
